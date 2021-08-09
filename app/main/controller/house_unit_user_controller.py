
#NEED TO CHANGE
import uuid
import datetime

from app.main import db
from app.main.model.user_company import UserCompany

def save_new_user_company(data):
    try:
        new_user_company = UserCompany(
            company_id=data['company_id'],
            user_id=data['user_id'],
            role=data['role']
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
def update_user_company(user_company_id, data):

    try:
        user_company = get_a_user_company(user_company_id)

        user_company.company_id=data['company_id'],
        user_company.user_id=data['user_id'],
        user_company.role=data['role'],
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

def delete_a_user_company(user_company_id):
    try:
        UserCompany.query.filter_by(id=user_company_id).delete()
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
def get_all_user_companies():

    return UserCompany.query.all()

def get_users_from_company(company_id):

    return UserCompany.query.filter_by(company_id=company_id).all()


def get_a_user_company(user_company_id):
    
    return UserCompany.query.filter_by(id=user_company_id).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()
