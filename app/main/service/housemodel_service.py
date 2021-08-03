import uuid
import datetime

from app.main import db
from app.main.model.housemodel import Housemodel

def save_new_housemodel(data):
    try:
        new_housemodel = Housemodel(
            houseunit_id=data['houseunit_id'],
            project_oneyear=data['project_oneyear'],
            project_twoyear=data['project_twoyear'],
            project_fiveyear=data['project_fiveyear'],
        )
        save_changes(new_housemodel)
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

def update_housemodel(housemodel_id, data):

    try:
        housemodel = get_a_housemodel(housemodel_id)

        housemodel.houseunit_id=data['houseunit_id'],
        housemodel.project_oneyear=data['project_oneyear'],
        housemodel.project_twoyear=data['project_twoyear'],
	housemodel.project_fiveyear=data['project_fiveyear'],

        save_changes(housemodel)

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

def delete_a_housemodel(housemodel_id):
    try:
        Housemodel.query.filter_by(id=housemodel_id).delete()
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

def get_all_housemodels(company_id=""):
    return Housemodel.query.all()


def get_a_Housemodel(housemodel_id):
    return Housemodel.query.filter_by(id=housemodel_id).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()