import uuid
import datetime

from app.main import db
from app.main.model.deal_note import DealNote

def save_new_deal_note(data):
    try:
        new_deal_note = DealNote(
            deal_id=data['deal_id'],
            note_id=data['note_id'],
        )
        save_changes(new_deal_note)
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


def get_notes_from_deal(deal_id):

    return DealNote.query.filter_by(deal_id=deal_id).all()


def get_a_deal_note(deal_note_id):
    return DealNote.query.filter_by(id=deal_note_id).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()
