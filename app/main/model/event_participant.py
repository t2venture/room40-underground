from .. import db, flask_bcrypt
import datetime
import jwt
from app.main.model.blacklist import BlacklistToken
from ..config import key

class EventParticipant(db.Model):
    """EventParticipant Model is used to link events to their respective participants"""
    __tablename__ = "event_participant"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    participant_id = db.Column(db.Integer, db.ForeignKey('user.id'))
