import uuid
import datetime

from app.main import db
from app.main.model.vote import Vote

def save_new_vote(deal_id, stage, name, data):
    try:
        new_vote = Vote(
            team=data['team'],
            team_notes=data['team_notes'],
            market=data['market'],
            market_notes=data['market_notes'],
            product=data['product'],
            product_notes=data['product_notes'],
            deal_id=data['deal_id'],
            name=data['name'],
            stage=data['stage']
        )
        db.session.add(new_vote)
        save_changes(new_vote)

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

    # vote_ids = []
    return Vote.query.all()


def get_a_vote(vote_id):
    return Vote.query.filter_by(id=vote_id).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()
