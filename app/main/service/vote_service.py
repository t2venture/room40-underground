import uuid
import datetime

from app.main import db
from app.main.model.vote import Vote
from app.main.service.deal_service import get_a_deal

def save_new_vote(deal_id, vote_type, data):
    try:
        new_vote = Vote(
            vote_field_1=data['vote_field_1'],
            vote_field_1_des=data['vote_field_1_des'],
        )
        db.session.add(new_vote)
        db.session.flush()

        save_changes(new_vote)
        deal = get_a_deal(deal_id)

        if(vote_type == 'initial'):
            deal.initial_vote_id = new_vote.id
        else:
            deal.final_vote_id = new_vote.id
        
        save_changes(deal)
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


def get_all_votes(deal_id):
    deal = get_a_deal(deal_id)

    vote_ids = [deal.initial_vote_id, deal.final_vote_id]

    return Vote.query.filter(Vote.id.in_(vote_ids)).all()


def get_a_vote(vote_id):
    return Vote.query.filter_by(id=vote_id).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()
