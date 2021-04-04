from .. import db, flask_bcrypt
import datetime
import jwt
from app.main.model.blacklist import BlacklistToken
from ..config import key

class Company(db.Model):
    """ Company Model for storing company related details """
    __tablename__ = "company"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.String(2500), unique=True, nullable=False)
    website = db.Column(db.String(255), unique=True, nullable=False)
    crunchbase = db.Column(db.String(255), unique=True, nullable=True)
    pitchbook = db.Column(db.String(255), unique=True, nullable=True)