import uuid
import datetime

from app.main import db

from app.main.model.document import Document
from app.main.model.property import Property
from app.main.model.user import User
from app.main.service.document_service import *
from app.main.service.property_service import *
from app.main.service.user_service import *

all_documents=get_all_deleted_documents(is_deleted=True)
all_users=get_all_deleted_users()
all_propertys=get_all_deleted_propertys()
time_now=datetime.datetime.utcnow()

#259200 is the number of seconds in 30 days
for doc in all_documents:
	delta=time_now-doc.modified_time
	if delta.total_seconds()>2592000:
		Document.query(id=doc.id).delete()
		db.session.commit()

for usr in all_users():
	delta=time_now-usr.modified_time
	if delta.total_seconds()>259200:
		User.query(id=usr.id).delete()
		db.session.commit()
for prop in all_propertys():
	delta=time_now-prop.modified_time
	if delta.total_seconds()>259200:
		Property.query(id=prop.id).delete()
		db.session.commit()