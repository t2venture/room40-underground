import uuid
import datetime

from app.main import db
from app.main.model.note import Note

def save_new_note(data):
    try:
        new_note = Note(
            description=data['description'],
            category=data['category'],
            is_thesis=bool(data['is_thesis']),
            deal_id=data['deal_id'],
            keywords=data['keywords']
        )
        save_changes(new_note)
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


def get_all_notes(deal_id="", search_query=""):
    
    notes = Note.query
    if deal_id is not "":
        notes = notes.filter_by(deal_id=deal_id)
    
    if search_query is not "":
        notes = notes.filter_by()
    
    # note_ids = [dn.note_id for dn in get_notes_from_deal(deal_id)]

    return Note.query.all()


def get_a_note(note_id):
    return Note.query.filter_by(id=note_id).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()
