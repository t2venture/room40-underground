import uuid
import datetime

from app.main import db
from app.main.model.assessment import Assessment

def save_new_assessment(company_id, data):
    try:
        new_assessment = Assessment(
            quarter=data['quarter'],
            sentiment=data['sentiment'],
            notes=data['notes'],
            company_id=data['company_id']
        )
        db.session.add(new_assessment)
        save_changes(new_assessment)

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


def get_all_assessments(company_id=""):

    assessments = Assessment.query
    
    if company_id and company_id != "":
        assessments = assessments.filter_by(company_id=company_id)

    return assessments.all()


def get_a_assessment(assessment_id):
    return Assessment.query.filter_by(id=assessment_id).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()
