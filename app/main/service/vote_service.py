import uuid
import datetime

from app.main import db
from app.main.model.vote import Vote

def save_new_vote(data):
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

def update_vote(vote_id, data):

    try:
        vote = get_a_vote(vote_id)

        vote.team = data['team']
        vote.team_notes=data['team_notes']
        vote.market=data['market']
        vote.market_notes=data['market_notes']
        vote.product=data['product']
        vote.product_notes=data['product_notes']
        vote.deal_id=data['deal_id'],
        vote.name=data['name'],
        vote.stage=data['stage']
        save_changes(vote)

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

def delete_a_vote(vote_id):
    try:
        Vote.query.filter_by(id=vote_id).delete()
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

def save_changes(data):
    db.session.add(data)
    db.session.commit()
