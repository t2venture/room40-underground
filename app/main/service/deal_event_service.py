import uuid
import datetime

from app.main import db
from app.main.model.deal_event import DealEvent

def save_new_deal_event(deal_id, event_id):
    try:
        new_deal_event = DealEvent(
            deal_id=deal_id,
            event_id=event_id,
        )
        save_changes(new_deal_event)
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


def get_events_from_deal(deal_id):

    return DealEvent.query.filter_by(deal_id=deal_id).all()


def get_a_deal_event(deal_event_id):
    return DealEvent.query.filter_by(id=deal_event_id).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()
