import uuid
import datetime

from app.main import db
from app.main.model.team_portfolio import TeamPortfolio

def save_new_team_portfolio(data):
    try:
        new_team_portfolio = TeamPortfolio(
            team_id=data['team_id'],
	    portfolio_id=data['portfolio_id']
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

        team_portfolio.team_id=data['team_id'],
        team_portfolio.portfolio_id=data['portfolio_id']

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

def delete_a_team_portfolio(team_portfolio_id):
    try:
        TeamPortfolio.query.filter_by(id=team_portfolio_id).delete()
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

def get_all_team_portfolios():
    return TeamPortfolio.query.all()

def get_teams_from_portfolio(portfolio_id):
    return TeamPortfolio.query.filter_by(portfolio_id=portfolio_id).all()

def get_portfolios_from_team(team_id):
    return TeamPortfolio.query.filter_by(team_id=team_id).all()

def get_a_team_portfolio(team_portfolio_id):
    return TeamPortfolio.query.filter_by(id=team_portfolio_id).first()

def save_changes(data):
    db.session.add(data)
    db.session.commit()