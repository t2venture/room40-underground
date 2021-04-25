import uuid
import datetime

from app.main import db
from app.main.model.event_participant import EventParticipant

def save_new_event_participant(data):
    try:
        new_event_participant = EventParticipant(
            event_id=data['event_id'],
            participant_id=data['participant_id'],
        )
        save_changes(new_event_participant)
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

def update_event_participant(event_participant_id, data):

    try:
        event_participant = get_a_event_participant(event_participant_id)

        event_participant.event_id=data['event_id'],
        event_participant.participant_id=data['participant_id']

        save_changes(event_participant)

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

def delete_a_event_participant(event_participant_id):
    try:
        EventParticipant.query.filter_by(id=event_participant_id).delete()
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

def get_all_event_participants():

    return EventParticipant.query.all()

def get_participants_from_event(event_id):

    return EventParticipant.query.filter_by(event_id=event_id).all()


def get_a_event_participant(event_participant_id):
    
    return EventParticipant.query.filter_by(id=event_participant_id).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()
