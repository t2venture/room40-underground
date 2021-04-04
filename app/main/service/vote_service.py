import uuid
import datetime

from app.main import db
from app.main.model.vote import Vote


def save_new_vote(data):
    new_user = User(
        vote_field_1 =data['vote_field_1']
        vote_field_1_des =data['vote_field_1_des']
    )
    save_changes(new_user)
    response_object = {
        'status': 'success',
        'message': 'Successfully registered.',
        'Authorization': auth_token
    }
    return response_object, 201


def get_all_users():
    return Vote.query.all()


def get_a_user(public_id):
    return User.query.filter_by(public_id=public_id).first()


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