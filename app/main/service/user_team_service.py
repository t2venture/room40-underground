import uuid
import datetime

from app.main import db
from app.main.model.user_team import UserTeam

def save_new_user_team(data):
    try:
        new_user_team = UserTeam(
            team_id=data['team_id'],
            user_id=data['user_id']
        )
        save_changes(new_user_team)
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
def update_user_team(user_team_id, data):

    try:
        user_team = get_a_user_team(user_team_id)

        user_team.team_id=data['team_id'],
        user_team.user_id=data['user_id'],
        save_changes(user_team)

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

def delete_a_user_team(user_team_id):
    try:
        UserTeam.query.filter_by(id=user_team_id).delete()
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
def get_all_user_teams():

    return UserTeam.query.all()

def get_users_from_team(team_id):

    return UserTeam.query.filter_by(team_id=team_id).all()

def get_teams_from_user(user_id):
    return UserTeam.query.filter_by(user_id=user_id).all()

def get_a_user_team(user_team_id):
    
    return UserTeam.query.filter_by(id=user_team_id).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()