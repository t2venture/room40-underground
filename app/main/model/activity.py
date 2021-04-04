from .. import db, flask_bcrypt
import datetime
import jwt
from app.main.model.blacklist import BlacklistToken
from ..config import key

class Activity(db.Model):
    """ Activity Model for storing activity related details """
    __tablename__ = "activity"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), unique=False, nullable=False)
    priority = db.Column(db.String(255), unique=False, nullable=False)
    due = db.Column(db.DateTime, nullable=False)
