import uuid
import datetime

from app.main import db
from app.main.model.user import User
from app.main.service.user_company_service import get_users_from_company

def save_new_user(data):
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        new_user = User(
            public_id=str(uuid.uuid4()),
            email=data['email'],
            username=data['username'],
            password=data['password'],
            registered_on=datetime.datetime.utcnow(),
            linkedin_url=data['linkedin_url'],
            twitter_url=data['twitter_url'],
        )
        save_changes(new_user)
        return generate_token(new_user)
    else:
        response_object = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return response_object, 409

def update_user(user_id, data):

    try:
        user = get_a_user(user_id)

        user.email=data['email'],
        user.username=data['username'],
        user.password=data['password'],
        user.linkedin_url=data['linkedin_url'],
        user.twitter_url=data['twitter_url'],
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

def delete_a_user(user_id):
    try:
        User.query.filter_by(id=user_id).delete()
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

def get_all_users(company_id=""):
    users=User.query

    if company_id and company_id != "":
        user_ids = [uc.user_id for uc in get_users_from_company(company_id)]
        users = users.filter(User.id.in_(user_ids))

    return users.all()


def get_a_user(user_id):
    return User.query.filter_by(id=user_id).first()


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