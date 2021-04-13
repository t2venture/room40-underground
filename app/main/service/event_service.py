import uuid
import datetime

from app.main import db
from app.main.model.event import Event
from app.main.service.deal_event_service import save_new_deal_event, get_events_from_deal

def save_new_event(deal_id, data):
    try:
        new_event = Event(
            time=datetime.datetime.strptime(data['time'], '%Y-%m-%dT%H:%M:%S'),
            link=data['link'],
            description=data['description'],
            notes=data['notes'],
            event_type=data['event_type'],
        )
        db.session.add(new_event)
        db.session.flush()
        data = {'deal_id': deal_id, 'event_id': new_event.id} 
        save_new_deal_event(data)
        save_changes(new_event)
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


def get_all_events(deal_id):
    event_ids = [de.event_id for de in get_events_from_deal(deal_id)]

    return Event.query.filter(Event.id.in_(event_ids)).all()


def get_a_event(event_id):
    return Event.query.filter_by(id=event_id).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()
