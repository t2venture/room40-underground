import uuid
import datetime

from app.main import db
from app.main.model.property_portfolio import PropertyPortfolio

def save_new_property_portfolio(data):
    try:
        new_property_portfolio = PropertyPortfolio(
            property_id=data['property_id'],
	    portfolio_id=data['portfolio_id']
        )
        save_changes(new_property_portfolio)
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

def update_property_portfolio(property_portfolio_id, data):

    try:
        property_portfolio = get_a_property_portfolio(property_portfolio_id)

        property_portfolio.property_id=data['property_id'],
        property_portfolio.portfolio_id=data['portfolio_id']

        save_changes(property_portfolio)

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

def delete_a_property_portfolio(property_portfolio_id):
    try:
        PropertyPortfolio.query.filter_by(id=property_portfolio_id).delete()
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

def get_all_property_portfolios(company_id=""):
    return PropertyPortfolio.query.all()

def get_a_property_portfolio(property_portfolio_id):
    return PropertyPortfolio.query.filter_by(id=property_portfolio_id).first()

def save_changes(data):
    db.session.add(data)
    db.session.commit()