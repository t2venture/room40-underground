import uuid
import datetime

from app.main import db
from app.main.model.portfolio import Portfolio

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

def get_all_portfolios():
    # Get all portfolios
    return Portfolio.query.all()


def get_a_portfolio(portfolio_id):
    return Portfolio.query.filter_by(id=portfolio_id).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()
