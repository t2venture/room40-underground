import uuid
import datetime

from app.main import db
from app.main.model.events_team import EventsTeam

def save_new_events_team(data):
	try:
		new_events_team=EventsTeam(
			team_id=data['portfolio_id'],
			description=data['description'],
			type=data['type'],
			created_time=datetime.datetime.utcnow(),
			is_deleted=False,
			is_active=True,
		)
		save_changes(new_events_team)
		response_object = {
			'status': 'success',
			'message': 'Successfully registered.'
			}
		return response_object, 201
	except Exception as e:
		print(e)
		response_object = {
			'status': 'fail',
			'message': 'Some error occurred. Please try again.'
			}
		return response_object, 401

def get_events_team_by_id(events_team_id):
	return EventsTeam.filter(EventsTeam.id==events_team_id).first()

def get_all_events_team_including_deleted():
	return EventsTeam.all()

def get_all_events_team():
	eventsteams=EventsTeam.all()
	eventsteams=eventsteams.filter(EventsTeam.is_active==True).filter(EventsTeam.is_deleted==False)
	return eventsteams.all()

def get_all_deleted_events_team():
	del_eventsteams=EventsTeam.all()
	del_eventsteams=del_eventsteams.filter(EventsTeam.is_deleted==False)
	return del_eventsteams.all()

def save_changes(data):
    db.session.add(data)
    db.session.commit()