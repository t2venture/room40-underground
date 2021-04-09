from .. import db, flask_bcrypt
import datetime
import jwt
from app.main.model.blacklist import BlacklistToken
from ..config import key

class UserCompany(db.Model):
    """UserCompany Model is used to link users to their respective companies"""
    __tablename__ = "user_company"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    role = db.Column(db.String(255), nullable=False)
