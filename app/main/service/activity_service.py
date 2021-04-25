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

def update_activity(activity_id, data):

    try:
        activity = get_a_activity(activity_id)

        activity.title=data['title'],
        activity.priority=data['priority'],
        activity.due=datetime.datetime.strptime(data['due'], '%Y-%m-%dT%H:%M:%S'),
        activity.company_id=data['company_id']

        save_changes(activity)

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

def delete_a_activity(activity_id):
    try:
        Activity.query.filter_by(id=activity_id).delete()
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

def get_all_activities(company_id="", due_date=None, priority="", title=""):

    activities = Activity.query

    if company_id and company_id != "":
        activities = activities.filter_by(company_id=company_id)

    if due_date and due_date != "":
        due_date_dt = datetime.datetime.strptime(due_date, '%Y-%m-%dT%H:%M:%S')
        activities = activities.filter(Activity.due <= due_date_dt)

    if priority and priority != "":
        activities = activities.filter(Activity.priority.ilike('%'+priority+'%'))

    if title and title != "":
        activities = activities.filter(Activity.title.ilike('%'+title+'%'))

    return activities.all()


def get_a_activity(activity_id):
    return Activity.query.filter_by(id=activity_id).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()
