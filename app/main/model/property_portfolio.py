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
