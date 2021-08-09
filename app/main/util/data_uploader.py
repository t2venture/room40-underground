import unittest
import datetime

from app.main import db
from app.main.model.deal import Deal
from app.main.model.company import Company
from app.main.model.user import User
from app.main.model.note import Note
from app.main.model.deal_investor import DealInvestor
from app.main.model.event_participant import EventParticipant
from app.main.model.user_company import UserCompany
from app.main.model.house_unit import HouseUnit
from app.main.util.projection import return_austin_houses, return_list_houseunit
import csv
users_csv = 'app/main/util/data_files/users.csv'
companies_csv = 'app/main/util/data_files/companies.csv'
deal_investors_csv = 'app/main/util/data_files/deal_investors.csv'
deals_csv = 'app/main/util/data_files/deals.csv'
events_csv = 'app/main/util/data_files/events.csv'
highlights_csv = 'app/main/util/data_files/highlights.csv'
notes_csv = 'app/main/util/data_files/notes.csv'
user_companies_csv = 'app/main/util/data_files/user_companies.csv'
votes_csv = 'app/main/util/data_files/votes.csv'  
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

def add_deals():
    with open(deals_csv, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            new_deal = Deal(
                stage=row["stage"],
                date=datetime.datetime.strptime(row['date'], '%Y-%m-%dT%H:%M:%S'),
                size=row["size"],
                post_money=row["post_money"],
                lead_id=row["lead_id"],
                company_id=row["company_id"],
            )
            db.session.add(new_deal)


def add_notes():
    with open(notes_csv, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            new_note = Note(
                description=row["description"],
                category=row["category"],
                is_thesis=bool(row["is_thesis"]),
                deal_id=row["deal_id"],
                keywords=','.join(row["keywords"].split("-"))
            )
            db.session.add(new_note)
    

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


def add_deal_investors():
    with open(deal_investors_csv, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            new_deal_investor = DealInvestor(
                deal_id=row["deal_id"],
                investor_id=row["investor_id"],
                amount=row["amount"],
                investment_type=row["investment_type"],
                fund_invested=row["fund_invested"]
            )
            db.session.add(new_deal_investor)

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
    print("uploading deals")
    add_deals()
    db.session.flush()
    print("uploading user companies")
    add_user_companies()
    db.session.flush()
    print("uploading deal investors")
    add_deal_investors()
    db.session.flush()
    print("uploading events")
    add_events()
    db.session.flush()
    print("uploading highlights")
    add_highlights()
    db.session.flush()
    print("uploading notes")
    add_notes()
    db.session.flush()
    print("uploading votes")
    add_votes()
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
    