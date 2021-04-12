import uuid
import datetime

from app.main import db
from app.main.model.activity import Activity
from app.main.service.company_activity_service import save_new_company_activity, get_activities_from_company

def save_new_activity(company_id, data):
    try:
        new_activity = Activity(
            title=data['title'],
            priority=data['priority'],
            due=datetime.datetime.strptime(data['due'], '%Y-%m-%dT%H:%M:%S'),
        )
        db.session.add(new_activity)
        db.session.flush()
        
        save_changes(new_activity)
        save_new_company_activity(company_id, new_activity.id)
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


def get_all_activities(company_id):

    activity_ids = []
    for ca in get_activities_from_company(company_id):
        if ca.activity_id is None:
            continue
        activity_ids.append(ca.activity_id)

    return Activity.query.filter(Activity.id.in_(activity_ids)).all()


def get_a_activity(company_id, activity_id):
    return Activity.query.filter_by(id=activity_id).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()
