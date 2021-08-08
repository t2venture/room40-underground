import uuid
import datetime

from app.main import db
from app.main.model.house_unit_user import HouseUnitUser

def save_new_house_unit_user(data):
    try:
        new_user_company = HouseUnitUser(
            house_unit_id=data['house_unit_id'],
            user_id=data['user_id'],
        )
        save_changes(new_user_company)
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

def update_house_unit_user(house_unit_user_id, data):

    try:
        user_company = get_a_house_unit_user(house_unit_user_id)

        user_company.house_unit_id=data['house_unit_id'],
        user_company.user_id=data['user_id'],
        save_changes(user_company)

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

def delete_a_house_unit_user(house_unit_user_id):
    try:
        HouseUnitUser.query.filter_by(id=house_unit_user_id).delete()
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

def get_a_house_unit_user(house_unit_user_id):
    return HouseUnitUser.query.filter_by(id=house_unit_user_id).first()

def get_all_house_unit_users():
    return HouseUnitUser.query.all()

def get_house_units_from_user(user_id):
    return HouseUnitUser.query.filter_by(user_id=user_id).all()

def save_changes(data):
    db.session.add(data)
    db.session.commit()