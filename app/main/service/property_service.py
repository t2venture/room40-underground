import uuid
import datetime

from app.main import db
from app.main.model.property import Property

def save_new_property(data):
    try:
        new_property = Property(
            majorcity=data['majorcity'],
            address=data['address'],
            building_sqft_area=data['building_sqft_area'],
            gross_sqft_area=data['gross_sqft_area'],
        )
        save_changes(new_property)
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

def update_property(property_id, data):

    try:
        property = get_a_property(property_id)

        property.majorcity=data['majorcity'],
        property.address=data['address'],
        property.building_sqft_area=data['building_sqft_area'],
        property.gross_sqft_area=data['gross_sqft_area'],

        save_changes(property)

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

def delete_a_property(property_id):
    try:
        Property.query.filter_by(id=property_id).delete()
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

def get_all_propertys():
    # Get all properties
    return Property.query.all()


def get_a_property(property_id):
    return Property.query.filter_by(id=property_id).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()
