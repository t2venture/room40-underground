import uuid
import datetime

from app.main import db
from app.main.model.user_team import UserTeam

def save_new_user_team(data):
    if 'role' not in data.keys():
        data['role']='Viewer'

    try:
        new_user_team = UserTeam(
            team_id=data['team_id'],
            user_id=data['user_id'],
            role=data['role'],
            created_by=data['login_user_id'],
            created_time=data['action_time'],
            modified_by=data['login_user_id'],
            modified_time=data['action_time'],
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
        if 'team_id' not in data.keys():
            data['team_id']=user_team.team_id
        if 'user_id' not in data.keys():
            data['user_id']=user_team.user_id
        user_team.team_id=data['team_id']
        user_team.user_id=data['user_id']
        if 'role' not in data.keys():
            data['role']=user_team.role
        user_team.role=data['role'],
        user_team.modified_by=data['login_user_id']
        user_team.modified_time=data['action_time']
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

def delete_a_user_team(user_team_id, data):
    try:
        usrtms=UserTeam.query.filter_by(id=user_team_id).all()
        for ut in usrtms:
            ut.is_deleted=True
            ut.modified_by=data['login_user_id']
            ut.modified_time=data['action_time']
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

def get_deleted_users_for_team(team_id):
    return UserTeam.query.filter_by(team_id=team_id).filter_by(is_deleted=True).all()

def get_deleted_teams_for_user(user_id):
    return UserTeam.query.filter_by(user_id=user_id).filter_by(is_deleted=True).all()

def get_all_deleted_user_teams():
    return UserTeam.query.filter_by(is_deleted=True).all()


def get_all_user_teams(is_active=True, is_deleted=False, user_id=1):
    usrtms=UserTeam.query
    if user_id!=1:
        usrtms=usrtms.filter_by(user_id=user_id)
    return usrtms.filter_by(is_deleted=False).filter_by(is_active=True).all()

def get_users_from_team(team_id):

    return UserTeam.query.filter_by(team_id=team_id).filter_by(is_active=True).filter_by(is_deleted=False).all()

def get_teams_from_user(user_id):
    return UserTeam.query.filter_by(user_id=user_id).filter_by(is_active=True).filter_by(is_deleted=False).all()

def get_a_user_team(user_team_id):
    
    return UserTeam.query.filter_by(id=user_team_id).filter_by(is_active=True).filter_by(is_deleted=False).first()

def check_user_in_team(user_id, team_id):
    data=UserTeam.query.filter_by(user_id=user_id).filter_by(team_id=team_id).all()
    if data is None:
        return False
    else:
        return True

def check_user_is_owner_or_editor(user_id, team_id):
    data=UserTeam.query.filter_by(user_id=user_id).filter_by(team_id=team_id).all()
    role=data['role']
    if role=='Owner' or role=='Editor':
        return True
    else:
        return False

def check_user_is_owner(user_id, team_id):
    data=UserTeam.query.filter_by(user_id=user_id).filter_by(team_id=team_id).all()
    role=data['role']
    if role=='Owner':
        return True
    else:
        return False


def save_changes(data):
    db.session.add(data)
    db.session.commit()