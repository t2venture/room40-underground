import uuid
import datetime

from app.main import db
from app.main.model.house_model import HouseModel

def save_new_house_model(data):
    try:
        new_house_model = HouseModel(
            houseunit_id=data['houseunit_id'],
            project_oneyear=data['project_oneyear'],
            project_twoyear=data['project_twoyear'],
            project_fiveyear=data['project_fiveyear'],
        )
        save_changes(new_house_model)
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

def update_house_model(house_model_id, data):

    try:
        house_model = get_a_house_model(house_model_id)

        house_model.houseunit_id=data['houseunit_id'],
        house_model.project_oneyear=data['project_oneyear'],
        house_model.project_twoyear=data['project_twoyear'],
        house_model.project_fiveyear=data['project_fiveyear'],

        save_changes(house_model)

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

def delete_a_house_model(house_model_id):
    try:
        HouseModel.query.filter_by(id=house_model_id).delete()
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

def get_all_house_models(company_id=""):
    return HouseModel.query.all()

def get_a_house_model(house_model_id):
    return HouseModel.query.filter_by(id=house_model_id).first()

def save_changes(data):
    db.session.add(data)
    db.session.commit()