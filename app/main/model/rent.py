from .. import db, flask_bcrypt
import datetime
import jwt
from app.main.model.blacklist import BlacklistToken
from ..config import key

class Rent(db.Model):
    """ Rent Model for storing rent related details """
    __tablename__ = "rent"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bedroom_count=db.Column(db.Integer, unique=False, nullable=False)
    bathroom_count=db.Column(db.Integer, unique=False, nullable=False)
    rounded_sqft_area=db.Column(db.Integer, unique=False, nullable=False)
    rent_amount=db.Column(db.Integer, unique=False, nullable=True)