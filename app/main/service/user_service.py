import uuid
import datetime

from app.main import db
from app.main.model.user import User
from app.main.model.user_team import UserTeam
from app.main.service.user_team_service import get_users_from_team
from app.main.service.team_service import save_new_team
def save_new_user(data):
    user = User.query.filter_by(email=data['email']).first()
    if 'linkedin_url' not in data.keys():
        linkedin_url=None
    else:
        linkedin_url=data['linkedin_url']
    if 'twitter_url' not in data.keys():
        twitter_url=None
    else:
        twitter_url=data['twitter_url']
    if 'profile_url' not in data.keys():
        profile_url=None
    else:
        profile_url=data['profile_url']
    if 'company_name' not in data.keys():
        company_name="Independent"
    else:
        company_name=data["company_name"]
    if not user:
        new_user = User(
            public_id=str(uuid.uuid4()),
            first_name=data['first_name'],
            last_name=data['last_name'],
            profile_url=profile_url,
            email=data['email'],
            username=data['username'],
            password=data['password'],
            company_name=company_name,
            registered_on=datetime.datetime.utcnow(),
            linkedin_url=linkedin_url,
            twitter_url=twitter_url,
            is_deleted=False,
            is_active=True,
            created_time=data['action_time'],
            modified_time=data['action_time'],
            modified_by=1,
            created_by=1,
        )
        save_changes(new_user)
        uid=new_user.id
        team_name="Personal Team"
        color='000000'
        new_data=dict()
        new_data["login_user_id"]=uid
        new_data["name"]=team_name
        new_data["action_time"]=datetime.datetime.utcnow()
        new_data["color"]=color
        save_new_team(new_data)
        return generate_token(new_user)
    else:
        response_object = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return response_object, 409

def update_user(user_id, data):
    try:
        user=get_a_user(user_id)
    except Exception as e:
        print(e)
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401    
    if 'linkedin_url' not in data.keys():
        linkedin_url=user.linkedin_url
    else:
        linkedin_url=data['linkedin_url']
    if 'twitter_url' not in data.keys():
        twitter_url=user.twitter_url
    else:
        twitter_url=data['twitter_url']
    if 'profile_url' not in data.keys():
        profile_url=user.profile_url
    else:
        profile_url=data['profile_url']
    if 'company_name' not in data.keys():
        company_name=user.company_name
    else:
        company_name=data["company_name"]
    if 'is_active' not in data.keys():
        is_active=True
    else:
        is_active=data['is_active']
    try:
        user = get_a_user(user_id)
        if 'email' not in data.keys():
            data['email']=user.email
        if 'username' not in data.keys():
            data['username']=user.username
        if 'password' not in data.keys():
            data['password']=user.password
        if 'first_name' not in data.keys():
            data['first_name']=user.first_name
        if 'last_name' not in data.keys():
            data['last_name']=user.last_name
        user.email=data['email'],
        user.username=data['username'],
        user.password=data['password'],
        user.linkedin_url=data['linkedin_url'],
        user.twitter_url=data['twitter_url'],
        user.first_name=data['first_name'],
        user.last_name=data['last_name'],
        user.profile_url=profile_url,
        user.linkedin_url=linkedin_url,
        user.twitter_url=twitter_url,
        user.is_active=is_active,
        user.company_name=company_name,
        user.modified_time=data['action_time'],
        user.modified_by=data['login_user_id']
        save_changes(user)

        response_object = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                }
        return response_object, 201

    except Exception as e:
        print(e)
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401

def delete_a_user(user_id, data):
    try:
        del_users=User.query.filter_by(id=user_id).all()
        for du in del_users:
            du.is_deleted=True
            du.modified_by=data['login_user_id']
            du.modified_time=data['action_time']
        db.session.commit()
        del_ut=UserTeam.query.filter_by(user_id=user_id).all()
        for dut in del_ut:
            dut.is_deleted=True
            dut.modified_by=data['login_user_id']
            dut.modified_time=data['action_time']
        db.session.commit()
        response_object = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                }
        return response_object, 201

    except Exception as e:
        print(e)
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401

def get_all_users(team_id="", is_deleted=False, is_active=True, company_name='', r_id=0):
    users=User.query.filter_by(is_deleted=is_deleted, is_active=is_active)
    if r_id:
        usr=get_a_user(r_id)
        company_name=usr.company_name
    if team_id and team_id!="":
        users_ids=[ut.user_id for ut in get_users_from_team(team_id)]
        users=users.filter(User.id.in_(users_ids))
    if company_name and company_name!="" and company_name!="Independent":
        company_name="%"+company_name+"%"
        users=users.filter(User.company_name.like(company_name))
    return users.all()

def check_same_company(id1, id2):
    user1=get_a_user(id1)
    user2=get_a_user(id2)
    if user1.company_name==user2.company_name:
        if user1.company_name!="Independent":  
            return True
    else:
        return False

def get_a_user(user_id):
    return User.query.filter_by(id=user_id).filter_by(is_deleted=False).filter_by(is_active=True).first()

def get_all_deleted_users():
    users=User.query.filter_by(is_deleted=True)
    return users.all()

def get_a_deleted_user(user_id):
    return User.query.filter_by(id=user_id).filter_by(is_deleted=True).first()

def save_changes(data):
    db.session.add(data)
    db.session.commit()

def generate_token(user):
    try:
        # generate the auth token
        auth_token = user.encode_auth_token(user.id)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.',
            'Authorization': auth_token
        }
        return response_object, 201
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401