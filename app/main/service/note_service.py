import uuid
import datetime

from app.main import db
from app.main.model.note import Note
from app.main.service.deal_note_service import save_new_deal_note, get_notes_from_deal

def save_new_note(deal_id, data):
    try:
        new_note = Note(
            description=data['description'],
            category=data['category'],
            is_thesis=bool(data['is_thesis']),
        )
        db.session.add(new_note)
        db.session.flush()
        data = {'deal_id': deal_id, 'note_id': new_note.id} 
        save_new_deal_note(data)
        save_changes(new_note)
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


def get_all_notes(deal_id):
    note_ids = [dn.note_id for dn in get_notes_from_deal(deal_id)]

    return Note.query.filter(Note.id.in_(note_ids)).all()


def get_a_note(note_id):
    return Note.query.filter_by(id=note_id).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()
