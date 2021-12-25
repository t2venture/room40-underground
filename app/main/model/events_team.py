from .. import db, flask_bcrypt
import datetime
import jwt
from app.main.model.blacklist import BlacklistToken
from ..config import key

class EventsTeam(db.Model):
	'''Team event model for storing all events at the team level'''
	__tablename__='events_team'
	id=db.Column(db.Integer, primary_key=True, autoincrement=True)
	team_id=db.Column(db.Integer, db.ForeignKey('team.id'))
	description=db.Column(db.Text(100000), unique=False, nullable=False)
	type=db.Column(db.String(30), unique=False, nullable=True)
	is_deleted=db.Column(db.Boolean, unique=False, nullable=False, default=False)
	is_active=db.Column(db.Boolean, unique=False, nullable=False, default=True)
	created_time=db.Column(db.DateTime, unique=False, nullable=False)
