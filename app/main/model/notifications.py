from .. import db, flask_bcrypt
import datetime
import jwt
from app.main.model.blacklist import BlacklistToken
from ..config import key

class Notifications(db.Model):
    """ Notifications Model for storing Notifications related details """
    __tablename__ = "notifications"
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    message=db.Column(db.String(500), nullable=False, unique=False)
    type=db.Column(db.Integer, nullable=False, unique=False)
    user_from=db.Column(db.Integer, nullable=True, unique=False)
    action_text=db.Column(db.String(100), nullable=True, unique=False)
    action_link=db.Column(db.String(100), nullable=True, unique=False)
    user_id=db.Column(db.Integer, nullable=True, unique=False)
    team_id=db.Column(db.Integer, nullable=True, unique=False)
    read=db.Column(db.Boolean, nullable=False, default=False)
    created_by=db.Column(db.Integer, unique=False, nullable=False)
    modified_by=db.Column(db.Integer, unique=False, nullable=False)
    created_time=db.Column(db.DateTime, unique=False, nullable=False)
    modified_time=db.Column(db.DateTime, unique=False, nullable=False)
    is_deleted=db.Column(db.Boolean, unique=False, nullable=False, default=False)
    is_active=db.Column(db.Boolean, unique=False, nullable=False, default=True)
