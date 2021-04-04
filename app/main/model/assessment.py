from .. import db, flask_bcrypt
import datetime
import jwt
from app.main.model.blacklist import BlacklistToken
from ..config import key

class Assessment(db.Model):
    """ Assessment Model for storing assessment related details """
    __tablename__ = "assessment"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quarter = db.Column(db.String(255), unique=False, nullable=False)
    assessment_field_1 = db.Column(db.String(255), unique=False, nullable=False)
    assessment_field_1_des = db.Column(db.String(255), unique=False, nullable=False)
