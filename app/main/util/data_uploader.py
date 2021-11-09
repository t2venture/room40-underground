from app.main.model.property_model import PropertyModel
import unittest
import datetime

from app.main import db
from app.main.model.user import User
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

#NEED TO REWRITE THIS USING UPDATED SCHEMA
def add_propertys():
    List_Property=return_list_property(return_raw_propertys())
    dict_of_values=obtain_dict_vals(obtain_time_series_dict(List_Property))
    train_list_of_med_val, train_list_of_max_val, train_list_of_min_val, test_list_of_med_val, test_list_of_max_val, test_list_of_min_val=obtain_train_test_lists(dict_of_values)
    autocorr_dict=obtain_autocorrs(train_list_of_med_val, test_list_of_med_val)
    for row in List_Property:
        timenow=datetime.datetime.utcnow()
        new_property=Property(address=row["address"], majorcity=row["majorcity"],
        building_sqft_area=row["building_sq_ft"], gross_sqft_area=row["gross_sq_ft"],
        latitude=row['latitude'], longitude=row['longitude'], street=row['street'], housenumber=row['housenumber'],
        usage_code=row['usage_code'], bd_rms=row["bed_count"], bt_rms=row["bath_count"], created_time=timenow, modified_time=timenow)
        db.session.add(new_property)
        db.session.flush()
        pid=new_property.id
        ##For other algorithms, change the name of project_arima from project_values file.
        fc1yr, fc2yr = project_arima(row["address"], train_list_of_med_val, test_list_of_med_val)
        ####5 yr forecast set to garbage
        fc5yr = 999999
        autocorr=autocorr_dict[row["address"]]
        m3ac=autocorr[3]
        m6ac=autocorr[6]
        new_property_model=PropertyModel(property_id=pid, project_oneyear=fc1yr,
        project_twoyear=fc2yr, project_5yr=fc5yr, threemonth_corr=m3ac, sixmonth_corr=m6ac, model_type="arima", created_time=timenow,
        modified_time=timenow)

        #New fields like model metrics need to be uploaded in scrape_property.
        db.session.add(new_property_model)
def upload_data():
    print("uploading users")
    add_users()
    db.session.flush()
    print ("uploading documents")
    add_documents()
    db.session.flush()
    '''
    print("uploading companies")
    add_companies()
    db.session.flush()
    print("uploading user companies")
    add_user_companies()
    db.session.flush()
    print("uploading propertys")
    ##JUST FOR TESTING
    #add_propertys()
    '''
    print("done")
    db.session.commit()


def clear_data():
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print('Clear table %s' % table)
        db.session.execute(table.delete())
    db.session.commit()
    