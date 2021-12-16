from app.main.model.property_model import PropertyModel
import unittest
import datetime
import random
from app.main import db
from app.main.model.user import User
from app.main.model.team import Team
from app.main.model.user_team import UserTeam
from app.main.model.property import Property
from app.main.model.document import Document
from app.main.util.scrape_property import obtain_autocorrs, obtain_train_test_lists, return_list_property, return_raw_propertys, obtain_time_series_dict, obtain_dict_vals, obtain_train_test_lists
from app.main.util.project_values import project_arima
from app.main.service.property_service import get_all_propertys
import uuid
import datetime
import csv
users_csv = 'app/main/util/data_files/users.csv'
from app.main.util.document_text import terms_use, terms_privacy
def add_users():
    new_user=User(email="angikar.ghosal@gmail.com",
    first_name="Angikar",
    last_name="Ghosal",
    profile_url=None,
    username="angikarghosal",
    admin=True,
    password="password",
    is_deleted=False,
    is_active=True,
    public_id=str(uuid.uuid4()),
    registered_on=datetime.datetime.utcnow(),
    linkedin_url=None,
    twitter_url=None,
    company_name="Independent",
    phonenumber='9194337673',
    created_by=1,
    modified_by=1,
    created_time=datetime.datetime.utcnow(),
    modified_time=datetime.datetime.utcnow(),
    confirmed=True,
    confirmed_on=datetime.datetime.utcnow()
    )
    db.session.add(new_user) 
    db.session.flush()

    new_team=Team(name="Superuser Personal Team",
    color="ffffff",
    created_by=1,
    modified_by=1,
    created_time=datetime.datetime.utcnow(),
    modified_time=datetime.datetime.utcnow(),
    is_deleted=False,
    is_active=True
    )
    db.session.add(new_team)
    db.session.flush()

    new_user_team=UserTeam(user_id=1,
    team_id=1,
    role='Owner',
    created_by=1,
    modified_by=1,
    created_time=datetime.datetime.utcnow(),
    modified_time=datetime.datetime.utcnow(),
    is_deleted=False,
    is_active=True)
    db.session.add(new_user_team)
    db.session.flush()

def add_documents():
    new_terms=Document(title="Terms of Use",
    contents=terms_use,
    created_by=1,
    modified_by=1,
    created_time=datetime.datetime.utcnow(),
    modified_time=datetime.datetime.utcnow(),
    is_deleted=False,
    is_active=True,
    )
    db.session.add(new_terms)
    new_privacy=Document(title="Privacy",
    contents=terms_privacy,
    created_by=1,
    modified_by=1,
    created_time=datetime.datetime.utcnow(),
    modified_time=datetime.datetime.utcnow(),
    is_deleted=False,
    is_active=True,
    )
    db.session.add(new_privacy)

def add_propertys():
    '''these are all dummy values'''
    market_value=random.randint(3500, 5000)*100
    ann_mortgage_cost = market_value/20
    estimated_rent = ann_mortgage_cost / 7
    hoa_fee = random.randint(400,800)
    hoa_rent = True
    est_property_tax = 0.0315 * market_value
    est_insurance= 0.007452 * market_value
    cap_rate = (estimated_rent - (ann_mortgage_cost/12) - hoa_fee - est_insurance - est_property_tax)/market_value
    yield_rate: cap_rate * random.randint(95,105)/100
    '''these are all dummy values'''
    List_Property=return_list_property(return_raw_propertys())
    #dict_of_values=obtain_dict_vals(obtain_time_series_dict(List_Property))
    #train_list_of_med_val, train_list_of_max_val, train_list_of_min_val, test_list_of_med_val, test_list_of_max_val, test_list_of_min_val=obtain_train_test_lists(dict_of_values)
    #autocorr_dict=obtain_autocorrs(train_list_of_med_val, test_list_of_med_val)
    for row in List_Property:
        new_property=Property(address=row["address"], majorcity=row["majorcity"],
        building_sqft_area=row["building_sq_ft"], gross_sqft_area=row["gross_sq_ft"],
        latitude=row['latitude'], longitude=row['longitude'], street=row['street'], housenumber=row['housenumber'],
        usage_code=row['usage_code'], bd_rms=row["bed_count"], bt_rms=row["bath_count"], created_by=1, modified_by=1,
        created_time=datetime.datetime.utcnow(), modified_time=datetime.datetime.utcnow(), is_deleted=False,
        is_active=True,
        market_price=market_value, ann_mortgage_cost=ann_mortgage_cost, cap_rate=cap_rate,
        yield_rate=yield_rate, lasso_score=random.randint(50,100), lasso_property=random.randint(50,100),
        lasso_economics=random.randint(50,100), lasso_location=random.randint(50,100), lasso_macro=random.randint(50,100),
        hoa_fee=hoa_fee, hoa_rent=hoa_rent, est_property_tax=est_property_tax, est_insurance=est_insurance)
        
        db.session.add(new_property)
        db.session.flush()
        '''
        pid=new_property.id
        ##For other algorithms, change the name of project_arima from project_values file.
        fc1yr, fc2yr = project_arima(row["address"], train_list_of_med_val, test_list_of_med_val)
        ####5 yr forecast set to garbage
        fc5yr = 999999
        autocorr=autocorr_dict[row["address"]]
        m3ac=autocorr[3]
        m6ac=autocorr[6]
        new_property_model=PropertyModel(property_id=pid, project_oneyear=fc1yr,
        project_twoyear=fc2yr, project_5yr=fc5yr, threemonth_corr=m3ac, sixmonth_corr=m6ac, model_type="arima",
        created_by=1, modified_by=1, created_time=datetime.datetime.utcnow(), modified_time=datetime.datetime.utcnow(), is_deleted=False,
        is_active=True)

        #New fields like model metrics need to be uploaded in scrape_property.
        db.session.add(new_property_model)
        '''
def upload_data():
    print("uploading users")
    add_users()
    db.session.flush()
    print ("uploading documents")
    add_documents()
    db.session.flush()
    print ("uploading properties")
    add_propertys()
    db.session.flush()
    print("done")
    db.session.commit()


def clear_data():
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print('Clear table %s' % table)
        db.session.execute(table.delete())
    db.session.commit()
    