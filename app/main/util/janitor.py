import uuid
import datetime

from app.main import db

time_param=2592000

from app.main.model.document import Document
from app.main.model.property import Property
from app.main.model.user import User
from app.main.model.team import Team
from app.main.model.user_team import UserTeam


from app.main.service.document_service import *
from app.main.service.property_service import *
from app.main.service.user_service import *
from app.main.service.team_service import *
from app.main.service.user_team_service import *

def clean_database():
	all_documents=get_all_deleted_documents()
	all_propertys=get_all_deleted_propertys()
	all_users=get_all_deleted_users()
	all_teams=get_all_deleted_teams()
	all_user_teams=get_all_deleted_user_teams()
	time_now=datetime.datetime.utcnow()

	#259200 is the number of seconds in 30 days
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
		delta=time_now=tm.modified_time
		if delta.total_seconds()>time_param:
			Team.query(id=tm.id).delete()
			db.session.commit()
	
	for utm in all_user_teams:
		delta=time_now=utm.modified_time
		if delta.total_seconds()>time_param:
			UserTeam.query(id=tm.id).delete()
			db.session.commit()
	