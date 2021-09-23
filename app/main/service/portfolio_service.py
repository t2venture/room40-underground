import uuid
import datetime

from app.main import db
from app.main.model.portfolio import Portfolio
from app.main.model.property_portfolio import PropertyPortfolio
from app.main.model.team_portfolio import TeamPortfolio
from app.main.service.property_portfolio_service import get_portfolios_from_property
from app.main.service.team_portfolio_service import get_portfolios_from_team, get_teams_from_portfolio

def save_new_portfolio(data):
    try:
        new_portfolio = Portfolio(
            title=data['title'],
            description=data['description'],
        )
        save_changes(new_portfolio)
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

def update_portfolio(portfolio_id, data):
    try:
        portfolio=get_a_portfolio(portfolio_id)
        portfolio.title=data['title'],
        portfolio.description=data['description'],
        save_changes(portfolio)
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


def delete_a_portfolio(portfolio_id):
    try:
        Portfolio.query.filter_by(id=portfolio_id).delete()
        db.session.commit()
        PropertyPortfolio.query.filter_by(portfolio_id=portfolio_id).delete()
        db.session.commit()
        TeamPortfolio.query.filter_by(portfolio_id=portfolio_id).delete()
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

def get_all_portfolios(property_id="", team_id=""):
    # Get all portfolios
    portfolios=Portfolio.query
    if property_id and property_id!="":
        portfolio_ids=[pt.portfolio_id for pt in get_portfolios_from_property(property_id)]
        portfolios=portfolios.filter(Portfolio.id.in_(portfolio_ids))
    if team_id and team_id!="":
        portfolios_ids=[tp.portfolio_id for tp in get_teams_from_portfolio(team_id)]
        portfolios=portfolios.filter(Portfolio.id.in_(portfolios_ids))
    return portfolios.all()


def get_a_portfolio(portfolio_id):
    return Portfolio.query.filter_by(id=portfolio_id).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()
 