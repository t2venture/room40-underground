import uuid
import datetime

from app.main import db
from app.main.model.team import Team
from app.main.model.user_team import UserTeam
from app.main.model.team_portfolio import TeamPortfolio
from app.main.service.user_team_service import get_teams_from_user
from app.main.service.team_portfolio_service import get_teams_from_portfolio


def save_new_team(data):
    try:
        new_team = Team(
            name=data['name'],
            company_id=data['company_id'],
        )
        save_changes(new_team)
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

    try:
        team = get_a_team(team_id)

        team.name=data['name'],
        team.company_id=data['company_id'],

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

def delete_a_team(team_id):
    try:
        Team.query.filter_by(id=team_id).delete()
        db.session.commit()
        UserTeam.query.filter_by(team_id=team_id).delete()
        db.session.commit()
        TeamPortfolio.query.filter_by(team_id=team_id).delete()
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

def get_all_teams(user_id="", portfolio_id=""):
    teams=Team.query
    if user_id and user_id!="":
        team_ids=[ut.team_id for ut in get_teams_from_user(user_id)]
        teams=teams.filter(Team.id.in_(team_ids))
    if portfolio_id and portfolio_id!="":
        teams_ids=[tp.team_id for tp in get_teams_from_portfolio(portfolio_id)]
        teams=teams.filter(Team.id.in_(teams_ids))
    return teams.all()


def get_a_team(team_id):
    return Team.query.filter_by(id=team_id).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()
