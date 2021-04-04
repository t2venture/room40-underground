from .. import db, flask_bcrypt
import datetime
import jwt
from app.main.model.blacklist import BlacklistToken
from ..config import key

class Vote(db.Model):
    """ Vote Model for storing vote related details """
    __tablename__ = "vote"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vote_field_1 = db.Column(db.String(255), unique=False, nullable=False)
    vote_field_1_des = db.Column(db.String(255), unique=False, nullable=False)
