import uuid
import datetime

from app.main import db
from app.main.model.company import Company

def save_new_company(data):
    try:
        new_company = Company(
            name=data['name'],
            description=data['description'],
            website=data['website'],
            industry=data['industry'],
            status=data['status'],
            crunchbase=data['crunchbase'],
            pitchbook=data['pitchbook'],
        )
        save_changes(new_company)
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


def get_all_companies():
    return Company.query.all()


def get_a_company(company_id):
    return Company.query.filter_by(id=company_id).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()
