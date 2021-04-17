import uuid
import datetime

from app.main import db
from app.main.model.highlight import Highlight
from app.main.service.company_highlight_service import save_new_company_highlight, get_highlights_from_company

def save_new_highlight(company_id, data):
    try:
        print(bool(data['is_active']))
        new_highlight = Highlight(
            notes=data['notes'],
            is_active=bool(data['is_active']),
        )
        db.session.add(new_highlight)
        db.session.flush()
        data = {'company_id': company_id, 'highlight_id': new_highlight.id} 
        save_new_company_highlight(data)
        save_changes(new_highlight)
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


def get_all_highlights(company_id):
    highlight_ids = [ch.highlight_id for ch in get_highlights_from_company(company_id)]

    return Highlight.query.filter(Highlight.id.in_(highlight_ids)).all()


def get_a_highlight(highlight_id):
    return Highlight.query.filter_by(id=highlight_id).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()
