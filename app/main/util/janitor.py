import uuid
import datetime

from app.main import db

time_param=2592000
short_time_param=172800

from app.main.model.document import Document
from app.main.model.property import Property
from app.main.model.user import User
from app.main.model.team import Team
from app.main.model.user_team import UserTeam
from app.main.model.team_portfolio import TeamPortfolio
from app.main.model.portfolio import Portfolio
from app.main.model.property_history import PropertyHistory
from app.main.model.property_model import PropertyModel
from app.main.model.property_portfolio import PropertyPortfolio
from app.main.model.events_portfolio import EventsPortfolio
from app.main.model.events_team import EventsTeam

from app.main.service.document_service import *
from app.main.service.property_service import *
from app.main.service.user_service import *
from app.main.service.team_service import *
from app.main.service.user_team_service import *
from app.main.service.team_portfolio_service import *
from app.main.service.portfolio_service import *
from app.main.service.property_history_service import *
from app.main.service.property_model_service import *
from app.main.service.property_portfolio_service import *
from app.main.service.events_portfolio_service import *
from app.main.service.events_team_service import *


def clean_database():
	all_documents=get_all_deleted_documents()
	all_propertys=get_all_deleted_propertys()
	all_users=get_all_deleted_users()
	all_teams=get_all_deleted_teams()
	all_user_teams=get_all_deleted_user_teams()
	all_team_portfolios=get_all_deleted_team_portfolios()
	all_portfolios=get_all_deleted_portfolios()
	all_property_historys=get_all_deleted_property_historys()
	all_property_models=get_all_deleted_property_models()
	all_property_portfolios=get_all_deleted_property_portfolios()
	all_users_notconfirmed=get_all_users()

	all_events_team_deleted=get_all_deleted_events_team()
	all_events_portfolio_deleted=get_all_deleted_events_portfolio()

	all_events_team=get_all_events_team()
	all_events_portfolio=get_all_events_portfolio()

	time_now=datetime.datetime.utcnow()

	#2592000 is the number of seconds in 30 days
	#172800 is the number of seconds in 2 days
	for u in all_users_notconfirmed:
		delta=time_now-u.modified_time
		if u.confirmed==False and delta.total_seconds()>time_param:
			User.query(id=u.id).delete()
			db.session.commit()

	for doc in all_documents:
		delta=time_now-doc.modified_time
		if delta.total_seconds()>time_param:
			Document.query(id=doc.id).delete()
			db.session.commit()

	for prop in all_propertys:
		delta=time_now-prop.modified_time
		if delta.total_seconds()>time_param:
			Property.query(id=prop.id).delete()
			db.session.commit()

	for usr in all_users:
		delta=time_now-usr.modified_time
		if delta.total_seconds()>time_param:
			User.query(id=usr.id).delete()
			db.session.commit()

	for tm in all_teams:
		delta=time_now-tm.modified_time
		if delta.total_seconds()>time_param:
			Team.query(id=tm.id).delete()
			db.session.commit()
	
	for utm in all_user_teams:
		delta=time_now-utm.modified_time
		if delta.total_seconds()>time_param:
			UserTeam.query(id=utm.id).delete()
			db.session.commit()

	for tpf in all_team_portfolios:
		delta=time_now-tpf.modified_time
		if delta.total_seconds()>time_param:
			TeamPortfolio.query(id=tpf.id).delete()
			db.session.commit()

	for pf in all_portfolios:
		delta=time_now-pf.modified_time
		if delta.total_seconds()>time_param:
			Portfolio.query(id=pf.id).delete()
			db.session.commit()

	for ph in all_property_historys:
		delta=time_now-ph.modified_time
		if delta.total_seconds()>time_param:
			PropertyHistory.query(id=ph.id).delete()
			db.session.commit()
	
	for pm in all_property_models:
		delta=time_now-pm.modified_time
		if delta.total_seconds()>time_param:
			PropertyModel.query(id=pm.id).delete()
			db.session.commit()

	for ppf in all_property_portfolios:
		delta=time_now-ppf.modified_time
		if delta.total_seconds()>time_param:
			PropertyPortfolio.query(id=ppf.id).delete()
			db.session.commit()

	for delevtm in all_events_team_deleted:
		delta=time_now-delevtm.created_time
		if delta.total_seconds()>time_param:
			EventsTeam.query(id=delevtm.id).delete()
			db.session.commit()

	for delevpf in all_events_portfolio_deleted:
		delta=time_now=delevpf.created_time
		if delta.total_seconds()>time_param:
			EventsPortfolio.query(id=delevpf.id).delete()
			db.session.commit()
		
	for evtm in all_events_team:
		delta=time_now-evtm.created_time
		if delta.total_seconds()>short_time_param:
			evtm.is_deleted=True
			db.session.add(evtm)
			db.session.commit()
	
	for evpf in all_events_portfolio:
		delta=time_now-evpf.created_time
		if delta.total_seconds()>short_time_param:
			evpf.is_deleted=True
			db.session.add(evtm)
			db.session.commit()

	

	
	