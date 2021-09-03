import unittest
import datetime

from app.main import db
from app.main.model.company import Company
from app.main.model.user import User
from app.main.model.user_company import UserCompany
from app.main.model.property import Property
from app.main.util.scrape_property import obtain_autocorrs, obtain_train_test_lists, return_list_property, return_raw_propertys, obtain_time_series_dict, obtain_dict_vals, obtain_train_test_lists
from app.main.util.project_values import project_arima

import csv
users_csv = 'app/main/util/data_files/users.csv'
companies_csv = 'app/main/util/data_files/companies.csv'
user_companies_csv = 'app/main/util/data_files/user_companies.csv'

def add_users():
    with open(users_csv, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            new_user = User(
                email=row["email"],
                password=row["password"],
                linkedin_url=row["linkedin_url"],
                twitter_url=row["twitter_url"],
                registered_on=datetime.datetime.utcnow(),
            )
            db.session.add(new_user)
    

def add_companies(): 
    with open(companies_csv, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            new_company = Company(
                name=row["name"],
                description=row["description"],
                website=row["website"],
                industry=row["industry"],
                status=row["status"],
                crunchbase=row["crunchbase"],
                pitchbook=row["pitchbook"]
            )
            db.session.add(new_company)


def add_user_companies():
    with open(user_companies_csv, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            new_user_company = UserCompany(
                user_id=row["user_id"],
                company_id=row["company_id"],
                role=row["role"]
            )
            db.session.add(new_user_company)


def add_propertys():
    List_Property=return_list_property(return_raw_propertys())
    dict_of_values=obtain_dict_vals(obtain_time_series_dict(List_Property))
    train_list_of_med_val, train_list_of_max_val, train_list_of_min_val, test_list_of_med_val, test_list_of_max_val, test_list_of_min_val=obtain_train_test_lists(dict_of_values)
    autocorr_dict=obtain_autocorrs(train_list_of_med_val, test_list_of_med_val)
    for row in List_Property:
        new_property=Property(address=row["address"], majorcity=row["majorcity"],
        building_sqft_area=row["building_sq_ft"], gross_sqft_area=row["gross_sq_ft"],
        latitude=row['latitude'], longitude=row['longitude'], street=row['street'], housenumber=row['housenumber'],
        usage_code=row['usage_code'], bd_rms=row["bed_count"], bt_rms=row["bath_count"])
        db.session.add(new_property)
    

def upload_data():
    print("uploading users")
    add_users()
    db.session.flush()
    print("uploading companies")
    add_companies()
    db.session.flush()
    print("uploading user companies")
    add_user_companies()
    db.session.flush()
    print("uploading propertys")
    add_propertys()
    print("done")
    db.session.commit()


def clear_data():
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print('Clear table %s' % table)
        db.session.execute(table.delete())
    db.session.commit()
    