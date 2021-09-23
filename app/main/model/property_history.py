from .. import db, flask_bcrypt
import datetime
import jwt
from app.main.model.blacklist import BlacklistToken
from ..config import key

class PropertyHistory(db.Model):
    """ Property History for storing property history related details """
    __tablename__ = "property_history"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    property_id=db.Column(db.Integer, db.ForeignKey('property.id'))
    prices=db.Column(db.String(5000), unique=False, nullable=True)
    #prices is going to be a stringified dict of history of prices
    events=db.Column(db.String(5000), unique=False, nullable=True)
    #events is also a stringified dict
    created_by=db.Column(db.Integer, db.ForeignKey('user.id'))
    modified_by=db.Column(db.Integer, db.ForeignKey('user.id'))
    created_time=db.Column(db.DateTime, unique=False, nullable=False)
    modified_time=db.Column(db.DateTime, unique=False, nullable=False)
    is_deleted=db.Column(db.Boolean, unique=False, nullable=False)
    is_active=db.Column(db.Boolean, unique=False, nullable=False)