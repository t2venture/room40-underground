import uuid
import datetime

from app.main import db
from app.main.model.vote import Vote
from app.main.service.deal_vote_service import save_new_deal_vote, get_votes_from_deal

def save_new_vote(deal_id, stage, name, data):
    try:
        new_vote = Vote(
            team=data['team'],
            team_notes=data['team_notes'],
            market=data['market'],
            market_notes=data['market_notes'],
            product=data['product'],
            product_notes=data['product_notes'],
        )
        db.session.add(new_vote)
        db.session.flush()

        save_changes(new_vote)
        data = {'deal_id': deal_id, 'vote_id': new_vote.id, 'stage': stage, 'name': name}     
        save_new_deal_vote(data)

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

    vote_ids = [dv.vote_id for dv in get_votes_from_deal(deal_id)]
    print(vote_ids)
    return Vote.query.filter(Vote.id.in_(vote_ids)).all()


def get_a_vote(vote_id):
    return Vote.query.filter_by(id=vote_id).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()
