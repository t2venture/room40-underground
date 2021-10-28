import uuid
import datetime

from app.main import db
from app.main.model.rent import Rent

def save_new_rent(data):
    try:
        new_rent = Rent(
            bedroom_count=data['bedroom_count'],
            bathroom_count=data['bathroom_count'],
            rounded_sqft_area=data['rounded_sqft_area'],
            rent_amount=data['rent_amount'],
        )
        save_changes(new_rent)
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

def update_rent(rent_id, data):

    try:
        rent = get_a_rent(rent_id)
        rent.bedroom_count=data['bedroom_count']
        rent.bathroom_count=data['bathroom_count']
        rent.rounded_sqft_area=data['rounded_sqft_area']
        rent.rent_amount=data['rent_amount']
        save_changes(rent)

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

def delete_a_rent(rent_id):
    try:
        Rent.query.filter_by(id=rent_id).delete()
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

def get_all_rents():
    return Rent.query.all()

def get_a_rent(rent_id):
    return Rent.query.filter_by(id=rent_id).first()

def save_changes(data):
    db.session.add(data)
    db.session.commit()