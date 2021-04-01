import psycopg2
import os
import uuid 
from datetime import datetime

CLEAR_TABLE = "DELETE FROM {}"
DROP_TABLE = "DROP TABLE {}"

CREATE_VOTE_TABLE = """CREATE TABLE vote (
    vote_id int PRIMARY KEY
    vote_field_1 int
    vote_field_1_description varchar(255)
)"""

CREATE_EVENT_TABLE = """CREATE TABLE event (
    event_id int PRIMARY KEY
    time datetime
    link varchar(255)
    description varchar(255)
    notes varchar(255)
    event_type int
)"""

CREATE_DEAL_EVENT_TABLE = """CREATE TABLE deal_event (
    deal_event_id int PRIMARY KEY
    deal_id int REFERENCES deal (deal_id)
    meeting_id int REFERENCES event (event_id)
)"""

CREATE_DEAL_TABLE = """CREATE TABLE deal (
    deal_id int PRIMARY KEY
    stage int,
    round_name varchar(255),
    size float,
    post_money float,
    initial_vote_id int REFERENCES vote (vote_id)
    final_vote_id int REFERENCES vote (vote_id)
    company_id int REFERENCES company (company_id)
    owner_id int REFERENCES user (user_id)
)"""

CREATE_EVENT_PARTICIPANT_TABLE = """CREATE TABLE event_participant (
    event_participant_id int PRIMARY KEY
    event_id int REFERENCES event (event_id)
    user_id int REFERENCES user (user_id)
)"""

CREATE_USER_TABLE = """CREATE TABLE user (
    user_id int PRIMARY KEY
    full_name varchar(255)
    email varchar(255)
    linkedin_url varchar(255)
    company_id int REFERENCES company (company_id)
)"""

CREATE_ROUND_INVESTOR_TABLE = """CREATE TABLE round_investor (
    round_investor_id int PRIMARY KEY
    amount float
    round_id int REFERENCES round (round_id)
    investor_id int REFERENCES user (user_id)
)"""

CREATE_DEAL_NOTE_TABLE = """CREATE TABLE deal_note (
    deal_note_id int PRIMARY KEY
    deal_id int REFERENCES deal (deal_id)
    note_id int REFERENCES note (note_id)
)"""

CREATE_NOTE_TABLE = """CREATE TABLE note (
    note_id in PRIMARY_KEY
    description varchar(255)
    category varchar(255)
    is_thesis boolean
)"""

CREATE_COMPANY_TABLE = """CREATE TABLE company (
    deal_id int PRIMARY KEY
    name varchar(255)
    description varchar(255)
    website varchar(255)
    post_valuation float
    pitchbook_url varchar(255)
    crunchbase_url varchar(255)
)"""

CREATE_COMPANY_ACTIVITY_TABLE = """CREATE TABLE company_activity (
    company_activity_id int PRIMARY KEY
    company_id int REFERENCES company (company_id)
    activity_id int REFERENCES activity (activity_id)
)"""

CREATE_COMPANY_ASSESSMENT_TABLE = """CREATE TABLE company_assessment (
    company_assessment_id int PRIMARY KEY
    company_id int REFERENCES company (company_id)
    assessment_id int REFERENCES assessment (assessment_id)
)"""

CREATE_ASSESSMENT_TABLE = """CREATE TABLE company_activity (
    assessment_id int PRIMARY KEY
    quarter varchar(255)
    assessment_field_1 varchar(255)
)"""

CREATE_ACTIVITY_TABLE = """CREATE TABLE activity (
    activity_id int PRIMARY KEY
    title varchar(255)
    priority int
    due datetime
)"""

ADD_ACTIVITY = "INSERT INTO activity (title, priority, due) values ('{}','{}','{}')"
ADD_ASSESSMENT = "INSERT INTO assessment (quarter, assessment_field_1) values ('{}','{}')"
ADD_NOTE = "INSERT INTO note (description, category, is_thesis) values ('{}','{}','{}')"
ADD_COMPANY = "INSERT INTO company (name, description, website, valuation, pitchbook_url, crunchbase_url) values ('{}','{}','{}','{}','{}','{}')"
ADD_DEAL = "INSERT INTO deal (stage, round_name, size, post_money, initial_vote_id, final_vote_id, company_id, owner_id) values ('{}','{}','{}','{}','{}','{}','{}','{}')"
ADD_USER = "INSERT INTO user (full_name, email, company_id, linkedin_url) values ('{}','{}','{}','{}')"
ADD_VOTE = "INSERT INTO vote (vote_field_1, vote_field_1_description) values ('{}','{}')"
ADD_EVENT = "INSERT INTO event (time, link, description, notes, event_type) values ('{}','{}','{}','{}','{}')"
ADD_COMPANY_ASSESSMENT  = "INSERT INTO company_assessment (company_id, assessment_id) values ('{}', '{}')"
ADD_COMPANY_ACTIVITY = "INSERT INTO company_activity (company_id, activity_id) values ('{}', '{}')"
ADD_DEAL_NOTE = "INSERT INTO deal_note (deal_id, note_id) values ('{}', '{}')"
ADD_ROUND_INVESTOR = "INSERT INTO round_investor (round_id, investor_id, amount) values ('{}','{}','{}')"
ADD_EVENT_PARTICIPANT = "INSERT INTO event_participant (event_id, user_id) values ('{}', '{}')"
ADD_DEAL_EVENT = "INSERT INTO deal_event (deal_id, meeting_id) values ('{}', '{}')"

def add_email(data):
    email = data.get("email") if data.get("email") is not None else ''
    landingPageId = data.get("landingPageId") if data.get("landingPageId") is not None else ''
    now = datetime.now()
    time = now.strftime("%d/%m/%Y %H:%M:%S")
    try:
        conn = psycopg2.connect(
                # database = os.getenv("DATABASE"),
                # user = os.getenv("USERNAME"),
                # password = os.getenv("PASSWORD"),
                # host = os.getenv("HOST"),
                # port = os.getenv("DATAPORT"),
                database = "der447s69tcb66",
                user = "veirluzsqkanmi",
                password = "0e01540c042256fae0efbfb765bd5377c60c54b56c2df6192598d380c45d928d",
                host = "ec2-54-237-143-127.compute-1.amazonaws.com",
                port = "5432"
            )
        cur = conn.cursor()
        cur.execute(ADD_EMAIL.format(email,landingPageId, time))
        conn.commit()
        cur.close()
        conn.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()

def create_table():
    try:
        conn = psycopg2.connect(
                # database = os.getenv("DATABASE"),
                # user = os.getenv("USERNAME"),
                # password = os.getenv("PASSWORD"),
                # host = os.getenv("HOST"),
                # port = os.getenv("DATAPORT")
                database = "der447s69tcb66",
                user = "veirluzsqkanmi",
                password = "0e01540c042256fae0efbfb765bd5377c60c54b56c2df6192598d380c45d928d",
                host = "ec2-54-237-143-127.compute-1.amazonaws.com",
                port = "5432"
            )
        cur = conn.cursor()
        cur.execute(CREATE_WAITLIST_TABLE)
        conn.commit()
        cur.close()
        conn.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()

def clear_table() :
    try:
        conn = psycopg2.connect(
                # database = os.getenv("DATABASE"),
                # user = os.getenv("USERNAME"),
                # password = os.getenv("PASSWORD"),
                # host = os.getenv("HOST"),
                # port = os.getenv("DATAPORT")
                database = "der447s69tcb66",
                user = "veirluzsqkanmi",
                password = "0e01540c042256fae0efbfb765bd5377c60c54b56c2df6192598d380c45d928d",
                host = "ec2-54-237-143-127.compute-1.amazonaws.com",
                port = "5432"
            )
        cur = conn.cursor()
        cur.execute(CLEAR_WAITLIST_TABLE)
        conn.commit()
        cur.close()
        conn.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()

def drop_tables():
    try:
        conn = psycopg2.connect(
                database = os.getenv("DATABASE"),
                user = os.getenv("USERNAME"),
                password = os.getenv("PASSWORD"),
                host = os.getenv("HOST"),
                port = os.getenv("DATAPORT")
            )
        cur = conn.cursor()
        cur.execute(DROP_WAITLIST_TABLE)
        conn.commit()
        cur.close()
        conn.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()

# drop_tables()
create_table()