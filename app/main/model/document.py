from .. import db, flask_bcrypt
import datetime
import jwt
from app.main.model.blacklist import BlacklistToken
from ..config import key

class Document(db.Model):
	'''Document model for storing documents'''
	__tablename__="document"
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	title=db.Column(db.String(255), unique=False, nullable=False)
	contents=db.Column(db.Text(100000), unique=False, nullable=False)
	created_by=db.Column(db.Integer, db.ForeignKey('user.id'))
	modified_by=db.Column(db.Integer, db.ForeignKey('user.id'))
	created_time=db.Column(db.DateTime, unique=False, nullable=False)
	modified_time=db.Column(db.DateTime, unique=False, nullable=False)
	is_deleted=db.Column(db.Boolean, unique=False, nullable=False)
	is_active=db.Column(db.Boolean, unique=False, nullable=False)