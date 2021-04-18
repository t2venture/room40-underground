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


def get_all_notes(deal_id="", search_query="", keyword_search="", thesis=False):
    
    notes = Note.query
    if deal_id and deal_id != "":
        notes = notes.filter_by(deal_id=deal_id)
        
    if search_query and search_query != "":
        notes = notes.filter(Note.description.ilike('%'+search_query+'%'))
    
    if keyword_search and keyword_search != "":
        notes = notes.filter(Note.keywords.ilike('%'+keyword_search+'%'))
   
    if thesis:
        notes = notes.filter_by(is_thesis=True)
    return notes.all()


def get_a_note(note_id):
    return Note.query.filter_by(id=note_id).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()
