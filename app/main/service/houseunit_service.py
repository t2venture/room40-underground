import uuid
import datetime

from app.main import db
from app.main.model.houseunit import Houseunit

def save_new_houseunit(data):
    try:
        new_houseunit = Houseunit(
            majorcity=data['majorcity'],
            address=data['address'],
            area=data['area'],
        )
        save_changes(new_houseunit)
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

def update_houseunit(houseunit_id, data):

    try:
        houseunit = get_a_houseunit(houseunit_id)

        houseunit.majorcity=data['houseunit'],
        houseunit.address=data['address'],
        houseunit.area=data['area'],

        save_changes(houseunit)

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

def delete_a_houseunit(houseunit_id):
    try:
        Houseunit.query.filter_by(id=houseunit_id).delete()
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

def get_all_houseunits():
    # Get all houseunits 
    return Houseunit.query.all()


def get_a_houseunit(houseunit_id):
    return Houseunit.query.filter_by(id=houseunit_id).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()
