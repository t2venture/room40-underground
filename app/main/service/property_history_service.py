import uuid
import datetime

from app.main import db
from app.main.model.property_history import PropertyHistory
import datetime

def save_new_property_history(data):
    try:
        new_property_history = PropertyHistory(
            property_id=data['property_id'],
	        prices=data['prices'],
	        events=data['events'],
            created_time=datetime.datetime.utcnow(),
            modified_time=datetime.datetime.utcnow(),
            is_deleted=False,
            is_active=True,
            created_by=1,
            modified_by=1,
        )
        save_changes(new_property_history)
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

def update_property_history(property_history_id, data):

    try:
        property_history = get_a_property_history(property_history_id)
        if 'property_id' not in data.keys():
            data['property_id']=property_history.property_id
        if 'prices' not in data.keys():
            data['prices']=property_history.prices
        if 'events' not in data.keys():
            data['events']=property_history.events
        property_history.property_id=data['property_id']
        property_history.prices=data['prices']
        property_history.events=data['events']
        property_history.modified_by=data['login_user_id']
        property_history.modified_time=data['action_time']
        save_changes(property_history)

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

def delete_a_property_history(property_history_id, data):
    try:
        del_phs=PropertyHistory.query.filter_by(id=property_history_id).all()
        for dph in del_phs:
            dph.is_deleted=True
            dph.modified_time=data['action_time']
            dph.modified_by=data['login_user_id']
            #should be 1
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

def get_all_property_historys(is_deleted=False, is_active=True, property_id=""):
    phs=PropertyHistory.query
    if property_id and property_id!="":
        phs=phs.filter_by(property_id=property_id)
    phs=phs.filter_by(is_deleted=False).filter_by(is_active=True).all()
    return phs

def get_all_deleted_property_historys():
    return PropertyHistory.query.filter_by(is_deleted=True).all()

def get_a_property_history(property_history_id):
    return PropertyHistory.query.filter_by(id=property_history_id).filter_by(is_deleted=False).filter_by(is_active=True).first()

def get_a_property_history_by_property_id(property_id):
    return PropertyHistory.query.filter_by(property_id=property_id).filter_by(is_deleted=False).filter_by(is_active=True).first()

def save_changes(data):
    db.session.add(data)
    db.session.commit()