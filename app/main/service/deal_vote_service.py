import uuid
import datetime

from app.main import db
from app.main.model.deal_vote import DealVote

def save_new_deal_vote(data):
    try:
        new_deal_vote = DealVote(
            deal_id=data['deal_id'],
            vote_id=data['vote_id'],
            stage=data['stage'],
            name = data['name']
        )
        save_changes(new_deal_vote)
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


def get_votes_from_deal(deal_id):
    return DealVote.query.filter_by(deal_id=deal_id).all()

def get_all_deal_votes():
    return DealVote.query.all()


def get_a_deal_vote(deal_vote_id):
    return DealVote.query.filter_by(id=deal_vote_id).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()
