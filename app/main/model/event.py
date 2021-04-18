from .. import db, flask_bcrypt
import datetime
import jwt
from app.main.model.blacklist import BlacklistToken
from ..config import key

class Event(db.Model):
    """ Event Model for storing event related details """
    __tablename__ = "event"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time = db.Column(db.DateTime, nullable=False)
    link = db.Column(db.String(255), unique=False, nullable=False)
    description = db.Column(db.String(1000), unique=False, nullable=False)
    notes = db.Column(db.String(2500), unique=False, nullable=False)
    event_type = db.Column(db.String(255), unique=False, nullable=False)
    deal_id = db.Column(db.Integer, db.ForeignKey('deal.id'))
    