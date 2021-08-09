import unittest
import datetime

from app.main import db
from app.main.model.company import Company
from app.main.model.user import User
from app.main.model.user_company import UserCompany
from app.main.model.house_unit import HouseUnit
from app.main.util.projection import return_austin_houses, return_list_houseunit
import csv
users_csv = 'app/main/util/data_files/users.csv'
companies_csv = 'app/main/util/data_files/companies.csv'
user_companies_csv = 'app/main/util/data_files/user_companies.csv'
house_units_csv = 'app/main/util/data_files/house_units.csv'

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


def add_house_units():
    List_HouseUnit=return_list_houseunit(return_austin_houses())
    for row in List_HouseUnit:
        new_houseunit=HouseUnit(address=row["address"], majorcity=row["majorcity"],
        building_sqft_area=row["building_sq_ft"], gross_sqft_area=row["gross_sq_ft"])
        db.session.add(new_houseunit)
# def add_housemodels():
    ###USE houseunit table to call function model and add the housemodel table

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
    print("uploading house_units")
    add_house_units()
    print("done")
    db.session.commit()


def clear_data():
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print('Clear table %s' % table)
        db.session.execute(table.delete())
    db.session.commit()
    