from .. import db, flask_bcrypt
import datetime
import jwt
from app.main.model.blacklist import BlacklistToken
from ..config import key

class Portfolio(db.Model):
	"Portfolio model for storing portfolio related details"
	__tablename__="portfolio"

	id=db.Column(db.Integer, primary_key=True, autoincrement=True)
	title=db.Column(db.String(255), unique=False, nullable=True)
	description=db.Column(db.String(255), unique=False, nullable=True)