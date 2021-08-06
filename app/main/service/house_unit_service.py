import uuid
import datetime

from app.main import db
from app.main.model.house_unit import HouseUnit

def save_new_house_unit(data):
    try:
        new_house_unit = HouseUnit(
            majorcity=data['majorcity'],
            address=data['address'],
            building_sqft_area=data['building_sqft_area'],
            gross_sqft_area=data['gross_sqft_area'],
        )
        save_changes(new_house_unit)
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

def update_house_unit(house_unit_id, data):

    try:
        house_unit = get_a_house_unit(house_unit_id)

        house_unit.majorcity=data['houseunit'],
        house_unit.address=data['address'],
        house_unit.building_sqft_area=data['building_sqft_area'],
        house_unit.gross_sqft_area=data['gross_sqft_area'],

        save_changes(house_unit)

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

def delete_a_house_unit(house_unit_id):
    try:
        HouseUnit.query.filter_by(id=house_unit_id).delete()
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

def get_all_house_units():
    # Get all houseunits 
    return HouseUnit.query.all()


def get_a_house_unit(house_unit_id):
    return HouseUnit.query.filter_by(id=house_unit_id).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()
