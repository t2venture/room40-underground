import uuid
import datetime

from app.main import db
from app.main.model.company_activity import CompanyActivity

def save_new_company_activity(company_id, activity_id):
    try:
        new_company_activity = CompanyActivity(
            activity_id=activity_id,
            company_id=company_id,
        )
        save_changes(new_company_activity)
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


def get_activities_from_company(company_id):

    return CompanyActivity.query.filter_by(company_id=company_id).all()


def get_a_company_activity(company_activity_id):
    return CompanyActivity.query.filter_by(id=company_activity_id).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()
