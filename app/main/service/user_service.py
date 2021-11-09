import uuid
import datetime

from app.main import db
from app.main.model.user import User
from app.main.model.user_team import UserTeam
from app.main.service.user_team_service import get_users_from_team
from app.main.service.team_service import save_new_team
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.main.token import generate_confirmation_token, confirm_token
from app.main.util.email import send_confirmation_email
import flask_bcrypt

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
    if 'username' not in data.keys():
        usrname=data['first_name']
    else:
        usrname=data['username']
    if 'phonenumber' not in data.keys():
        phone='999999999'
    else:
        phone=data['phonenumber']
    if validate_email(data['email'])==True or validate_first_name(data['first_name'])==True:
        response_object = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return response_object, 409
    if not user:
        new_user = User(
            public_id=str(uuid.uuid4()),
            first_name=data['first_name'],
            last_name=data['last_name'],
            profile_url=profile_url,
            email=data['email'],
            username=usrname,
            password=data['password'],
            company_name=company_name,
            registered_on=datetime.datetime.utcnow(),
            linkedin_url=linkedin_url,
            twitter_url=twitter_url,
            phonenumber=phone,
            is_deleted=False,
            is_active=True,
            created_time=data['action_time'],
            modified_time=data['action_time'],
            modified_by=1,
            created_by=1,
            confirmed=False
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
        #confirmation_token=generate_confirmation_token(data["email"])
        #send_confirmation_email(data["email"], confirmation_token)
        
        #WE COULD POTENTIALLY LIMIT OPERATIONS UNLESS USER IS CONFIRMED. CURRENTLY CONFIRMATION NOT NEEDED.
        
    else:
        response_object = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return response_object, 409

def update_password_user(user_id, new_password):
    try:
        user=get_a_user(user_id)
    except Exception as e:
        print(e)
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401   
    user.password_hash=flask_bcrypt.generate_password_hash(new_password).decode('utf-8')
    save_changes(user)

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
    if 'password' in data.keys():
        update_password_user(user_id, data['password']) 
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
        if 'first_name' not in data.keys():
            data['first_name']=user.first_name
        if 'last_name' not in data.keys():
            data['last_name']=user.last_name
        if 'confirmed' not in data.keys():
            data['confirmed']=user.confirmed
        if 'confirmed_on' not in data.keys():
            data['confirmed_on']=user.confirmed_on
        if 'phonenumber' not in data.keys():
            data['phonenumber']=user.phonenumber
        user.email=data['email']
        user.username=data['username']
        user.first_name=data['first_name']
        user.last_name=data['last_name']
        user.profile_url=profile_url
        user.linkedin_url=linkedin_url
        user.twitter_url=twitter_url
        user.is_active=is_active
        user.company_name=company_name
        user.phonenumber=data['phonenumber']
        user.modified_time=data['action_time']
        user.modified_by=data['login_user_id']
        user.confirmed=data['confirmed']
        user.confirmed_on=data['confirmed_on']
        save_changes(user)
        response_object = {
                    'status': 'success',
                    'message': 'Successfully registered changes to user.',
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

def get_all_users(deleted=False, active=True, adm=False, usr=1):
    users=User.query.filter_by(is_deleted=deleted).filter_by(is_active=active)
    if (adm==False):
        users=users.filter(User.id==usr)
    return users.all()

def check_same_company(id1, id2):
    user1=get_a_user(id1)
    user2=get_a_user(id2)
    if user1.company_name==user2.company_name:
        if user1.company_name!="Independent":  
            return True
    else:
        return False

def check_if_registered_user(email):
    usrs=User.query.filter(User.email==email).filter_by(is_deleted=False).filter_by(is_active=True).all()
    if not usrs:
        return False
    else:
        return True

def get_a_user_by_email(email):
    return User.query.filter(User.email==email).filter_by(is_deleted=False).filter_by(is_active=True).first()


def get_a_user(user_id):
    return User.query.filter(User.id==user_id).filter_by(is_deleted=False).filter_by(is_active=True).first()

def get_all_deleted_users():
    users=User.query.filter_by(is_deleted=True)
    return users.all()

def get_a_deleted_user(user_id):
    return User.query.filter_by(id=user_id).filter_by(is_deleted=True).first()

def save_changes(data):
    db.session.add(data)
    db.session.commit()

def validate_first_name(first_name):
    user = User.query.filter(User.first_name==first_name).first()
    if user:
        return True
    else:
        return False

def validate_email(email):
    user = User.query.filter(User.email==email).first()
    if user:
        return True
    else:
        return False

def generate_token(user):
    try:
        # generate the auth token
        auth_token = user.encode_auth_token(user.id)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered. Please confirm your email.',
            'Authorization': auth_token
        }
        return response_object, 201
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401

def confirm_email(token):
    try:
        email = confirm_token(token)
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'The confirmation token has expired or is not valid.'
        }
        return response_object, 401
    user_to_confirm = User.query.filter(User.email==email).first()
    id_of_user_to_confirm=user_to_confirm.id
    data={"confirmed":True, "confirmed_on":datetime.datetime.utcnow(), "action_time": datetime.datetime.utcnow(), "login_user_id": id_of_user_to_confirm}
    return update_user(id_of_user_to_confirm, data)

def verify_reset_email(token, password):
    try:
        email = confirm_token(token)
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'The confirmation token has expired or is not valid.'
        }
        return response_object, 401
    user_to_change_password=User.query.filter(User.email==email).first()
    if (user_to_change_password):
        id_of_user_to_reset=user_to_change_password.id
        data={"modified_by":id_of_user_to_reset, "modified_time":datetime.datetime.utcnow(),"password": password, "confirmed":True, "confirmed_on":datetime.datetime.utcnow(), "action_time": datetime.datetime.utcnow(), "login_user_id": id_of_user_to_reset}
        return update_user(id_of_user_to_reset, data)
    else:
        response_object = {
            'status': 'fail',
            'message': 'The email does not correspond to a registered user.'
        }
        return response_object, 401
    
    