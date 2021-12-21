from .. import db, flask_bcrypt
import datetime
import jwt
from app.main.model.blacklist import BlacklistToken
from ..config import key

class TeamPortfolio(db.Model):
	"""Team Portfolio model for storing which team accesses which portfolio"""
	__tablename__="team_portfolio"
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	team_id=db.Column(db.Integer, db.ForeignKey('team.id'))
	portfolio_id=db.Column(db.Integer, db.ForeignKey('portfolio.id'))
	role=db.Column(db.String(50), unique=False, nullable=False, default='Viewer')
	is_deleted=db.Column(db.Boolean, unique=False, nullable=False, default=False)
	is_active=db.Column(db.Boolean, unique=False, nullable=False, default=True)
	created_by=db.Column(db.Integer, db.ForeignKey('user.id'))
	modified_by=db.Column(db.Integer, db.ForeignKey('user.id'))
	created_time=db.Column(db.DateTime, unique=False, nullable=False)
	modified_time=db.Column(db.DateTime, unique=False, nullable=False)