from .. import db, flask_bcrypt
import datetime
import jwt
from app.main.model.blacklist import BlacklistToken
from ..config import key

class Property(db.Model):
    """ Property Model for storing deal related details """
    __tablename__ = "property"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    majorcity=db.Column(db.String(255), unique=False, nullable=False)
    address=db.Column(db.String(255), unique=False, nullable=False)
    building_sqft_area=db.Column(db.Integer, unique=False, nullable=True)
    gross_sqft_area=db.Column(db.Integer, unique=False, nullable=True)
    latitude=db.Column(db.Float, unique=False, nullable=False)
    longitude=db.Column(db.Float, unique=False, nullable=False)
    street=db.Column(db.String(255), unique=False, nullable=True)
    housenumber=db.Column(db.String(255), unique=False, nullable=True)