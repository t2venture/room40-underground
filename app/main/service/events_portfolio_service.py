import uuid
import datetime

from app.main import db
from app.main.model.events_portfolio import EventsPortfolio

def save_new_events_portfolio(data):
	try:
		new_events_portfolio=EventsPortfolio(
			portfolio_id=data['portfolio_id'],
			description=data['description'],
			type=data['type'],
			created_time=datetime.datetime.utcnow(),
			is_deleted=False,
			is_active=True,
		)
		save_changes(new_events_portfolio)
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

def get_events_portfolio_by_id(events_portfolio_id):
	return EventsPortfolio.filter(EventsPortfolio.id==events_portfolio_id).first()

def get_all_events_portfolio_including_deleted():
	return EventsPortfolio.all()

def get_all_events_portfolio():
	eventsportfolios=EventsPortfolio.all()
	eventsportfolios=eventsportfolios.filter(EventsPortfolio.is_active==True).filter(EventsPortfolio.is_deleted==False)
	return eventsportfolios.all()

def get_all_deleted_events_portfolio():
	del_eventsportfolios=EventsPortfolio.all()
	del_eventsportfolios=del_eventsportfolios.filter(EventsPortfolio.is_deleted==False)
	return del_eventsportfolios.all()

def save_changes(data):
    db.session.add(data)
    db.session.commit()