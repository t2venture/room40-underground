import uuid
import datetime

from app.main import db
from app.main.model.property_portfolio import PropertyPortfolio

def save_new_property_portfolio(data):
    try:
        new_property_portfolio = PropertyPortfolio(
            property_id=data['property_id'],
	        portfolio_id=data['portfolio_id'],
            created_by=data['login_user_id'],
            modified_by=data['login_user_id'],
            is_active=True,
            is_deleted=False,
            created_time=data['action_time'],
            modified_time=data['action_time']
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
        if 'property_id' not in data.keys():
            data['property_id']=property_portfolio.property_id
        if 'portfolio_id' not in data.keys():
            data['portfolio_id']=property_portfolio.portfolio_id
        property_portfolio.property_id=data['property_id']
        property_portfolio.portfolio_id=data['portfolio_id']
        property_portfolio.modified_by=data['login_user_id']
        property_portfolio.modified_time=data['action_time']
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

def delete_a_property_portfolio(property_portfolio_id, data):
    try:
        dppfs=PropertyPortfolio.query.filter_by(id=property_portfolio_id).all()
        for ppf in dppfs:
            ppf.is_deleted=True
            ppf.modified_time=data["action_time"]
            ppf.modified_by=data["login_user_id"]
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

def get_all_property_portfolios(is_deleted=False, is_active=True):
    return PropertyPortfolio.query.filter_by(is_deleted=False).filter_by(is_active=True).all()

def get_all_deleted_property_portfolios():
    return PropertyPortfolio.query.filter_by(is_deleted=True).all()

def get_propertys_from_portfolio(portfolio_id):
    return PropertyPortfolio.query.filter_by(portfolio_id=portfolio_id).filter_by(is_deleted=False).filter_by(is_active=True).all()

def get_portfolios_from_property(property_id):
    return PropertyPortfolio.query.filter_by(property_id=property_id).filter_by(is_deleted=False).filter_by(is_active=True).all()

def get_a_property_portfolio(property_portfolio_id):
    return PropertyPortfolio.query.filter_by(id=property_portfolio_id).filter_by(is_deleted=False).filter_by(is_active=True).first()

def save_changes(data):
    db.session.add(data)
    db.session.commit()