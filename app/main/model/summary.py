from .. import db, flask_bcrypt
import datetime
import jwt
from app.main.model.blacklist import BlacklistToken
from ..config import key

class Summary(db.Model):
	"""Summary model for storing summary related details"""
	__tablename__ ="summary"
	id=db.Column(db.Integer, primary_key=True, autoincrement=True)
	zipcode=db.Column(db.String(15), unique=False, nullable=False)
	total_units=db.Column(db.Integer, unique=False, default=0)
	low_curr_frac=db.Column(db.Float, unique=False, default=0.0)
	high_curr_frac=db.Column(db.Float, unique=False, default=0.0)
	low_proj1_frac=db.Column(db.Float, unique=False, default=0.0)
	high_proj1_frac=db.Column(db.Float, unique=False, default=0.0)
	low_proj2_frac=db.Column(db.Float, unique=False, default=0.0)
	high_proj2_frac=db.Column(db.Float, unique=False, default=0.0)
	created_by=db.Column(db.Integer, db.ForeignKey('user.id'))
	modified_by=db.Column(db.Integer, db.ForeignKey('user.id'))
	created_time=db.Column(db.DateTime, unique=False, nullable=False)
	modified_time=db.Column(db.DateTime, unique=False, nullable=False)