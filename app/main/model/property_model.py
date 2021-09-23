from .. import db, flask_bcrypt
import datetime
import jwt
from app.main.model.blacklist import BlacklistToken
from ..config import key

class PropertyModel(db.Model):
    """ Property Model for storing Property model related details """
    __tablename__ = "property_model"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    property_id=db.Column(db.Integer, db.ForeignKey('property.id'))
    model_type=db.Column(db.String(30), unique=False, nullable=False)
    project_oneyear = db.Column(db.Float, unique=False, nullable=False)
    project_twoyear = db.Column(db.Float, unique=False, nullable=False)
    project_fiveyear = db.Column(db.Float, unique=False, nullable=False)
    threemonth_corr=db.Column(db.Float, unique=False, nullable=False)
    sixmonth_corr=db.Column(db.Float, unique=False, nullable=False)
    lower_series=db.Column(db.String(511), unique=False, nullable=True)
    median_series=db.Column(db.String(511), unique=False, nullable=True)
    upper_series=db.Column(db.String(511), unique=False, nullable=True)
    model_metrics=db.Column(db.String(1023), unique=False, nullable=True)
    created_by=db.Column(db.Integer, db.ForeignKey('user.id'))
    modified_by=db.Column(db.Integer, db.ForeignKey('user.id'))
    created_time=db.Column(db.DateTime, unique=False, nullable=False)
    modified_time=db.Column(db.DateTime, unique=False, nullable=False)
    is_deleted=db.Column(db.Boolean, unique=False, nullable=False)
    is_active=db.Column(db.Boolean, unique=False, nullable=False)