import uuid
import datetime

from app.main import db
from app.main.model.deal import Deal

def save_new_deal(data):
    try:
        new_deal = Deal(
            stage=data['stage'],
            name=data['name'],
            size=data['size'],
            post_money=data['post_money'],
            lead_id=data['lead_id'],
            company_id=data['company_id'],
        )
        save_changes(new_deal)
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


def get_all_deals(company_id=""):
    # Get all deals for a company
    # Get current valuation of company
    # Get a company's stake in another company
    # Get the current companies cap table
    # Get the return on investment for companies
    return Deal.query.all()


def get_a_deal(deal_id):
    return Deal.query.filter_by(id=deal_id).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()
