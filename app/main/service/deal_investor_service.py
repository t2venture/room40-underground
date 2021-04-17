import uuid
import datetime

from app.main import db
from app.main.model.deal_investor import DealInvestor

def save_new_deal_investor(data):
    try:
        new_deal_investor = DealInvestor(
            deal_id=data['deal_id'],
            investor_id=data['investor_id'],
            amount=data['amount'],
            date=datetime.datetime.strptime(data['date'], '%Y-%m-%dT%H:%M:%S'),
            investment_type=data['investment_type'],
            fund_invested=data['fund_invested'],
        )
        save_changes(new_deal_investor)
        response_object = {
                'status': 'success',
                'message': 'Successfully registered.',
            }
        return response_object, 201

    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401

def get_all_deal_investors():

    return DealInvestor.query.all()

def get_investors_from_deal(deal_id):

    return DealInvestor.query.filter_by(deal_id=deal_id).all()


def get_a_deal_investor(deal_investor_id):
    return DealInvestor.query.filter_by(id=deal_investor_id).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()
