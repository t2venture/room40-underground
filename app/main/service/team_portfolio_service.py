import uuid
import datetime

from app.main import db
from app.main.model.team_portfolio import TeamPortfolio

def save_new_team_portfolio(data):
    try:
        if 'role' not in data.keys():
            data['role']='Viewer'
        new_team_portfolio = TeamPortfolio(
            team_id=data['team_id'],
	    portfolio_id=data['portfolio_id'],
        role=data['role'],
        created_by=data['login_user_id'],
        modified_by=data['login_user_id'],
        created_time=data['action_time'],
        modified_time=data['action_time'],
        is_deleted=False,
        is_active=True,
        )
        save_changes(new_team_portfolio)
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

def update_team_portfolio(team_portfolio_id, data):

    try:
        team_portfolio = get_a_team_portfolio(team_portfolio_id)
        if 'role' not in data.keys():
            data['role']=team_portfolio.role
        team_portfolio.team_id=data['team_id']
        team_portfolio.portfolio_id=data['portfolio_id']
        team_portfolio.role=data['role']
        save_changes(team_portfolio)

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

def delete_a_team_portfolio(team_portfolio_id, data):
    try:
        dtps=TeamPortfolio.query.filter_by(id=team_portfolio_id).all()
        for dtp in dtps:
            dtp.is_deleted=True
            dtp.modified_time=data['action_time']
            dtp.modified_by=data['login_user_id']
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

def get_all_team_portfolios(is_deleted=False, is_active=True):
    return TeamPortfolio.query.filter_by(is_deleted=False).filter_by(is_active=True).all()

def get_all_deleted_team_portfolios():
    return TeamPortfolio.query.filter_by(is_deleted=True)

def get_teams_from_portfolio(portfolio_id):
    return TeamPortfolio.query.filter_by(portfolio_id=portfolio_id).filter_by(is_active=True).filter_by(is_deleted=False).all()

def get_portfolios_from_team(team_id):
    return TeamPortfolio.query.filter_by(team_id=team_id).filter_by(is_active=True).filter_by(is_deleted=False).all()

def get_a_team_portfolio(team_portfolio_id):
    return TeamPortfolio.query.filter_by(id=team_portfolio_id).filter_by(is_active=True).filter_by(is_deleted=False).first()

def save_changes(data):
    db.session.add(data)
    db.session.commit()