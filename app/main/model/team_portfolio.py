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
