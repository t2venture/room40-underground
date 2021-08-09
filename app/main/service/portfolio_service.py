import uuid
import datetime

from app.main import db
from app.main.model.portfolio import Portfolio

def save_new_portfolio(data):
    try:
        new_property = Portfolio(
            title=data['title'],
            description=data['description'],
        )
        save_changes(new_property)
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
