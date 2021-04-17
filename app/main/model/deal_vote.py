from .. import db, flask_bcrypt
import datetime
import jwt
from app.main.model.blacklist import BlacklistToken
from ..config import key

class DealVote(db.Model):
    """DealVote Model is used to link votes to their respective deals"""
    __tablename__ = "deal_vote"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    deal_id = db.Column(db.Integer, db.ForeignKey('deal.id'))
    vote_id = db.Column(db.Integer, db.ForeignKey('vote.id'))
    stage = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)