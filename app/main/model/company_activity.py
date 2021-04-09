from .. import db, flask_bcrypt
import datetime
import jwt
from app.main.model.blacklist import BlacklistToken
from ..config import key

class CompanyActivity(db.Model):
    """ CompanyActivity Model is used to link companies to their respective activities """
    __tablename__ = "company_activity"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
