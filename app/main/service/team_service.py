import uuid
import datetime

from app.main import db
from app.main.model.team import Team
from app.main.model.user_team import UserTeam
from app.main.model.team_portfolio import TeamPortfolio
from app.main.service.user_team_service import check_user_in_team, get_teams_from_user
from app.main.service.team_portfolio_service import get_teams_from_portfolio
from app.main.service.user_team_service import save_new_user_team

def save_new_team(data):
    if 'color' not in data.keys():
        color='000000'
    else:
        color=data['color']
    
    try:
        new_team = Team(
            name=data['name'],
            color=color,
            is_deleted=False,
            is_active=True,
            created_time=data['action_time'],
            modified_time=data['action_time'],
            modified_by=data['login_user_id'],
            created_by=data['login_user_id'],
        )
        save_changes(new_team)
        tid=new_team.id
        new_data=dict()
        new_data['team_id']=tid
        new_data['user_id']=data['login_user_id']
        new_data['role']='Owner'
        save_new_user_team(new_data)
        ###ADD TEAM FOR EVERY INDIVIDUAL
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

def update_team(team_id, data):
    if 'is_active' not in data.keys():
        is_active=True
    else:
        is_active=data['is_active']
    try:
        team = get_a_team(team_id)

        team.name=data['name'],
        team.is_active=is_active,
        if 'name' not in data.keys():
            data['name']=team.name
        team.name=data['name']
        if 'color' not in data.keys():
            data['color']=team.color
        team.color=data['color']
        team.modified_time=data['action_time']
        team.modified_by=data['login_user_id']
        save_changes(team)
    
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

def delete_a_team(team_id, data):
    try:
        del_teams=Team.query.filter_by(id=team_id).all()
        for dt in del_teams:
            dt.is_deleted=True
            dt.modified_by=data['login_user_id']
            dt.modified_time=data['action_time']
        db.session.commit()
        duts=UserTeam.query.filter_by(team_id=team_id).all()
        for dut in duts:
            dut.is_deleted=True
            dut.modified_by=data['login_user_id']
            dut.modified_time=data['action_time']
        db.session.commit()
        dtpfs=TeamPortfolio.query.filter_by(team_id=team_id).all()
        for tpf in dtpfs:
            tpf.is_deleted=True
            tpf.modified_time=data['action_time']
            tpf.modified_by=data['modified_by']
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

def get_personal_team_id(user_id):
    user_teams=UserTeam.query.filter_by(is_active=True).filter_by(is_deleted=False).filter_by(user_id=user_id).all()
    utids=[ut.team_id for ut in user_teams]
    personal_teams=Team.query.filter(Team.name.like("Personal Team")).filter_by(is_active=True).filter_by(is_deleted=False)
    personal_teams=personal_teams.filter(Team.id.in_(utids))
    return personal_teams.first()



def get_all_teams(user_id=1, portfolio_id="", is_active=True, is_deleted=False):
    teams=Team.query.filter_by(is_active=True).filter_by(is_deleted=False)
    if user_id!=1:
        team_ids=[ut.team_id for ut in get_teams_from_user(user_id)]
        teams=teams.filter(Team.id.in_(team_ids))
    if portfolio_id and portfolio_id!="":
        teams_ids=[tp.team_id for tp in get_teams_from_portfolio(portfolio_id)]
        teams=teams.filter(Team.id.in_(teams_ids))
    return teams.all()

def get_all_deleted_teams():
    return Team.query.filter_by(is_deleted=True).all()


def get_a_team(team_id):
    return Team.query.filter_by(id=team_id).filter_by(is_active=True).filter_by(is_deleted=False).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()
