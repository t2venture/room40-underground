from .. import db, flask_bcrypt
import datetime
import jwt
from app.main.model.blacklist import BlacklistToken
from ..config import key

class PropertyModel(db.Model):
    """ Deal Model for storing deal related details """
    __tablename__ = "property_model"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    property_id=db.Column(db.Integer, db.ForeignKey('property.id'))
    project_oneyear = db.Column(db.Integer, unique=False, nullable=False)
    project_twoyear = db.Column(db.Integer, unique=False, nullable=False)
    project_fiveyear = db.Column(db.Integer, unique=False, nullable=False)
    threemonth_corr=db.Column(db.Float, unique=False, nullable=False)
    sixmonth_corr=db.Column(db.Float, unique=False, nullable=False)