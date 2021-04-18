from .. import db, flask_bcrypt
import datetime
import jwt
from app.main.model.blacklist import BlacklistToken
from ..config import key

class Vote(db.Model):
    """ Vote Model for storing vote related details """
    __tablename__ = "vote"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    team = db.Column(db.Integer, unique=False, nullable=False)
    team_notes = db.Column(db.String(255), unique=False, nullable=False)
    market = db.Column(db.Integer, unique=False, nullable=False)
    market_notes = db.Column(db.String(255), unique=False, nullable=False)
    product = db.Column(db.Integer, unique=False, nullable=False)
    product_notes = db.Column(db.String(255), unique=False, nullable=False)
    name=db.Column(db.String(255), unique=False, nullable=False)
    stage=db.Column(db.String(255), unique=False, nullable=False)
    deal_id=db.Column(db.Integer,db.ForeignKey('deal.id'))