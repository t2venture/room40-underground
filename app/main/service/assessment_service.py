import uuid
import datetime

from app.main import db
from app.main.model.assessment import Assessment
from app.main.service.company_assessment_service import save_new_company_assessment, get_assessments_from_company

def save_new_assessment(company_id, data):
    try:
        new_assessment = Assessment(
            quarter=data['quarter'],
            sentiment=data['sentiment'],
            notes=data['notes'],
        )
        db.session.add(new_assessment)
        db.session.flush()
        
        save_changes(new_assessment)
        data = {'company_id': company_id, 'assessment_id': new_assessment.id} 
        save_new_company_assessment(data)
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


def get_all_assessments(company_id):
    assessment_ids = []
    for ca in get_assessments_from_company(company_id):
        if ca.assessment_id is None:
            continue
        assessment_ids.append(ca.assessment_id)

    return Assessment.query.filter(Assessment.id.in_(assessment_ids)).all()


def get_a_assessment(company_id, assessment_id):
    return Assessment.query.filter_by(id=assessment_id).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()
