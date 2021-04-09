from .. import db, flask_bcrypt
import datetime
import jwt
from app.main.model.blacklist import BlacklistToken
from ..config import key

class Deal(db.Model):
    """ Deal Model for storing deal related details """
    __tablename__ = "deal"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    stage = db.Column(db.String(255), unique=False, nullable=False)
    name = db.Column(db.String(255), unique=False, nullable=False)
    size = db.Column(db.Integer, unique=False, nullable=False)
    post_money = db.Column(db.Integer, unique=False, nullable=False)
    lead_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    initial_vote_id = db.Column(db.Integer, db.ForeignKey('vote.id'))
    final_vote_id = db.Column(db.Integer, db.ForeignKey('vote.id'))