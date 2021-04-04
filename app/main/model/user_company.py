from .. import db, flask_bcrypt
import datetime
import jwt
from app.main.model.blacklist import BlacklistToken
from ..config import key

class UserCompany(db.Model):
    """EventParticipant Model is used to link events to their respective participants"""
    __tablename__ = "event_participant"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    company_id = db.Column(db.Integer, ForeignKey('company.id'))
    role = db.Column(db.String(255), nullable=False)
