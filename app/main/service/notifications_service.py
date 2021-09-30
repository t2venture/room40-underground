import uuid
import datetime

from app.main import db
from app.main.model.notifications import Notifications
from app.main.service.team_service import get_personal_team_id

def save_new_notifications(data):
	if 'user_from' not in data.keys():
		data['user_from']=1
	if 'team_id' not in data.keys():
		pteam=get_personal_team_id(data['user_id'])
		data['team_id']=pteam['id']
	if 'action_text' not in data.keys():
		data['action_text']=''
	if 'action_link' not in data.keys():
		data['action_link']=''
	try:
		new_notifications=Notifications(
			message=data['message'],
			type=data['message'],
			user_from=data['user_from'],
			action_text=data['action_text'],
			action_link=data['action_link'],
			user_id=data['user_id'],
			team_id=data['team_id'],
			created_by=1,
			modified_by=1,
			created_time=data['action_time'],
			modified_time=data['action_time'],
			is_deleted=False,
			is_active=True,
		)
		save_changes(new_notifications)
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

def get_a_notification(notification_id):
	return Notifications.filter_by(id=notification_id).filter_by(is_active=True).filter_by(is_deleted=False).first()

def get_all_notifications_for_user(user_id):
	return Notifications.filter_by(user_id=user_id).filter_by(is_active=True).filter_by(is_deleted=False).all()

def get_all_deleted_notifications_for_user(user_id):
	return Notifications.filter_by(user_id=user_id).filter_by(is_deleted=True).all()


def mark_read_notifications(notification_id, data):
	login_user=data['login_user_id']
	notification=get_a_notification(notification_id)
	if notification.user_id != login_user:
		response_object = {
			'status': 'fail',
                	'message': 'You cannot update this information.'
			}
                return response_object, 401
	notification.read=True
	notification.modified_by=data['login_user_id']
	notification.modified_time=data['action_time']
	save_changes(notification)
	response_object = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                }
        return response_object, 201

def mark_unread_notifications(notification_id, data):
	login_user=data['login_user_id']
	notification=get_a_notification(notification_id)
	if notification.user_id != login_user:
		response_object = {
			'status': 'fail',
                	'message': 'You cannot update this information.'
			}
                return response_object, 401
	notification.read=False
	notification.modified_by=data['login_user_id']
	notification.modified_time=data['action_time']
	save_changes(notification)
	response_object = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                }
        return response_object, 201

def check_if_read(notification_id):
	notification=get_a_notification(notification_id)
	return (notification.read)

def update_a_notification(notification_id, data):
	if 'is_active' not in data.keys():
		is_active=True
	else:
		is_active=data['is_active']
	try:
		notification=get_a_notification(notification_id)
		notification.is_active=is_active
		if 'message' in data.keys():
			notification.message=data['message']
		if 'type' in data.keys():
			notification.type=data['type']
		if 'user_from' in data.keys():
			notification.user_from=data['user_from']
		if 'action_text' in data.keys():
			notification.action_text=data['action_text']
		if 'action_link' in data.keys():
			notification.action_link=data['action_link']
		notification.modified_by=data['login_user_id']
		notification.modified_time=data['action_time']
		save_changes(notification)
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

def delete_a_notification(notification_id, data):
	try:
		notification=get_a_notification(notification_id)
		notification.is_deleted=True
		notification.modified_by=data['login_user_id']
		notification.modified_time=data['action_time']
		save_changes(notification)
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


def save_changes(data):
    db.session.add(data)
    db.session.commit()
