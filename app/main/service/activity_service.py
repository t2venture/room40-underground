import uuid
import datetime

from app.main import db
from app.main.model.activity import Activity

def save_new_activity(data):
    try:
        new_activity = Activity(
            title=data['title'],
            priority=data['priority'],
            due=datetime.datetime.strptime(data['due'], '%Y-%m-%dT%H:%M:%S'),
            company_id=data['company_id']
        )
        db.session.add(new_activity)
        save_changes(new_activity)

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


def get_all_activities(company_id=""):
    
    return Activity.query.all()


def get_a_activity(activity_id):
    return Activity.query.filter_by(id=activity_id).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()
