from .. import db, flask_bcrypt
import datetime
import jwt
from app.main.model.blacklist import BlacklistToken
from ..config import key

class Team(db.Model):
    """Team Model for storing team related details """
    __tablename__ = "team"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=False, nullable=False, default="Personal Team")
    color = db.Column(db.String(7), unique=False, nullable=False, default='000000')
    #black is the default color
    created_by=db.Column(db.Integer, db.ForeignKey('user.id'))
    modified_by=db.Column(db.Integer, db.ForeignKey('user.id'))
    created_time=db.Column(db.DateTime, unique=False, nullable=False)
    modified_time=db.Column(db.DateTime, unique=False, nullable=False)
    is_deleted=db.Column(db.Boolean, unique=False, nullable=False)
    is_active=db.Column(db.Boolean, unique=False, nullable=False)