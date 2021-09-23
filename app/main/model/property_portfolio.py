from .. import db, flask_bcrypt
import datetime
import jwt
from app.main.model.blacklist import BlacklistToken
from ..config import key

class PropertyPortfolio(db.Model):
	"""Property Portfolio model for storing which property goes to which portfolio"""
	__tablename__="property_portfolio"
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	property_id=db.Column(db.Integer, db.ForeignKey('property.id'))
	portfolio_id=db.Column(db.Integer, db.ForeignKey('portfolio.id'))
	created_by=db.Column(db.Integer, db.ForeignKey('user.id'))
	modified_by=db.Column(db.Integer, db.ForeignKey('user.id'))
	created_time=db.Column(db.DateTime, unique=False, nullable=False)
	modified_time=db.Column(db.DateTime, unique=False, nullable=False)
	is_deleted=db.Column(db.Boolean, unique=False, nullable=False)
	is_active=db.Column(db.Boolean, unique=False, nullable=False)
