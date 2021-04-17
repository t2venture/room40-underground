import uuid
import datetime

from app.main import db
from app.main.model.company_assessment import CompanyAssessment

def save_new_company_assessment(data):
    try:
        print(data)
        new_company_assessment = CompanyAssessment(
            assessment_id=data['assessment_id'],
            company_id=data['company_id'],
        )
        save_changes(new_company_assessment)
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


def get_assessments_from_company(company_id):

    return CompanyAssessment.query.filter_by(company_id=company_id).all()


def get_a_company_assessment(company_assessment_id):
    return CompanyAssessment.query.filter_by(id=company_assessment_id).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()
