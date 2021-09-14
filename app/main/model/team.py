from .. import db, flask_bcrypt
import datetime
import jwt
from app.main.model.blacklist import BlacklistToken
from ..config import key

class Team(db.Model):
    """Team Model for storing team related details """
    __tablename__ = "team"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=False, nullable=False)