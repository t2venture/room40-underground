import uuid
import datetime

from app.main import db
from app.main.model.property_model import PropertyModel

def save_new_property_model(data):
    try:
        new_property_model = PropertyModel(
            property_id=data['property_id'],
            project_oneyear=data['project_oneyear'],
            project_twoyear=data['project_twoyear'],
            project_fiveyear=data['project_fiveyear'],
            threemonth_corr=data['threemonth_corr'],
            sixmonth_corr=data['sixmonth_corr'],
            noise=data['noise'],
        )
        save_changes(new_property_model)
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

def update_property_model(property_model_id, data):

    try:
        property_model = get_a_property_model(property_model_id)

        property_model.property_id=data['property_id'],
        property_model.project_oneyear=data['project_oneyear'],
        property_model.project_twoyear=data['project_twoyear'],
        property_model.project_fiveyear=data['project_fiveyear'],
        property_model.threemonth_corr=data['threemonth_corr'],
        property_model.sixmonth_corr=data['sixmonth_corr'],
        property_model.noise=data['noise'],
        save_changes(property_model)

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

def delete_a_property_model(property_model_id):
    try:
        PropertyModel.query.filter_by(id=property_model_id).delete()
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

def get_all_property_models():
    return PropertyModel.query.all()

def get_a_property_model(property_model_id):
    return PropertyModel.query.filter_by(id=property_model_id).first()

def save_changes(data):
    db.session.add(data)
    db.session.commit()