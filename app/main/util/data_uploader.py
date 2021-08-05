import unittest
import datetime

from app.main import db
from app.main.model.activity import Activity
from app.main.model.assessment import Assessment
from app.main.model.deal import Deal
from app.main.model.company import Company
from app.main.model.event import Event
from app.main.model.highlight import Highlight
from app.main.model.user import User
from app.main.model.vote import Vote
from app.main.model.note import Note
from app.main.model.deal_investor import DealInvestor
from app.main.model.event_participant import EventParticipant
from app.main.model.user_company import UserCompany
from app.main.model.house_unit import HouseUnit

import csv
users_csv = 'app/main/util/data_files/users.csv'
activities_csv = 'app/main/util/data_files/activities.csv'
assessments_csv = 'app/main/util/data_files/assessments.csv'
companies_csv = 'app/main/util/data_files/companies.csv'
deal_investors_csv = 'app/main/util/data_files/deal_investors.csv'
deals_csv = 'app/main/util/data_files/deals.csv'
events_csv = 'app/main/util/data_files/events.csv'
highlights_csv = 'app/main/util/data_files/highlights.csv'
notes_csv = 'app/main/util/data_files/notes.csv'
user_companies_csv = 'app/main/util/data_files/user_companies.csv'
votes_csv = 'app/main/util/data_files/votes.csv'  
houseunits_csv = 'app/main/util/data_files/houseunits.csv'

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

def add_activities():
    with open(activities_csv, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            new_activity = Activity(
                title=row["title"],
                priority=row["priority"],
                due=datetime.datetime.strptime(row['due'], '%Y-%m-%dT%H:%M:%S'),
                company_id=row["company_id"],
            )
            db.session.add(new_activity)
    

def add_assessments():
    with open(assessments_csv, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            new_assessment = Assessment(
                quarter=row["quarter"],
                sentiment=row["sentiment"],
                notes=row["notes"],
                company_id=row["company_id"],
            )
            db.session.add(new_assessment)
    

def add_events():
    with open(events_csv, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            new_event = Event(
                time=datetime.datetime.strptime(row['time'], '%Y-%m-%dT%H:%M:%S'),
                link=row["link"],
                description=row["description"],
                notes=row["notes"],
                event_type=row["event_type"],
                deal_id=row["deal_id"],
            )
            db.session.add(new_event)
            db.session.flush()
            participants = row["participant_ids"].split('-')
            for p in participants:
                new_event_participant = EventParticipant(
                    event_id=new_event.id,
                    participant_id=p
                )
    

def add_highlights():
    with open(highlights_csv, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            new_highlight = Highlight(
                is_active=bool(row["is_active"]),
                notes=row["notes"],
                company_id=row["company_id"],
            )
            db.session.add(new_highlight)
    

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
    

def add_votes():
    with open(votes_csv, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            new_vote = Vote(
                team=row["team"],
                team_notes=row["team_notes"],
                market=row["market"],
                market_notes=row["market_notes"],
                product=row["product"],
                product_notes=row["product_notes"],
                deal_id=row["deal_id"],
                stage=row["stage"],
                name=row["name"]
            )
            db.session.add(new_vote)


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

def add_houseunits():
    with open(houseunits_csv, mode='r') as csv_file:
        csv_reader=csv.DictReader(csv_file)
        for row in csv_reader:
            new_houseunit=Houseunit(
                address=row["address"],
                majorcity=row["majorcity"],
                area=row["area"]
            )
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
    print("uploading activities")
    add_activities()
    db.session.flush()
    print("uploading assessments")
    add_assessments()
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
    print("done")
    db.session.commit()


def clear_data():
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print('Clear table %s' % table)
        db.session.execute(table.delete())
    db.session.commit()
    