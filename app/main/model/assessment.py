from .. import db, flask_bcrypt
import datetime
import jwt
from app.main.model.blacklist import BlacklistToken
from ..config import key

class Assessment(db.Model):
    """ Assessment Model for storing assessment related details """
    __tablename__ = "assessment"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quarter = db.Column(db.String(20), unique=False, nullable=False)
    sentiment = db.Column(db.Integer, unique=False, nullable=False)
    notes = db.Column(db.String(2000), unique=False, nullable=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))