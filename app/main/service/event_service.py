import uuid
import datetime

from app.main import db
from app.main.model.event import Event

def save_new_event(data):
    try:
        new_event = Event(
            time=datetime.datetime.strptime(data['time'], '%Y-%m-%dT%H:%M:%S'),
            link=data['link'],
            description=data['description'],
            notes=data['notes'],
            event_type=data['event_type'],
            deal_id=data['deal_id']
        )
        db.session.add(new_event)
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


def get_all_events(deal_id="", week=False):
    events = Event.query
    if week:
        start_date=datetime.datetime.now()
        end_date = datetime.datetime.now()
        while end_date.weekday() != 4:
            end_date += datetime.timedelta(1)
        events = events.filter(Event.time >= start_date).filter(Event.time <= end_date)
        
    return events.all()


def get_a_event(event_id):
    return Event.query.filter_by(id=event_id).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()
