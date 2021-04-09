from .. import db, flask_bcrypt
import datetime
import jwt
from app.main.model.blacklist import BlacklistToken
from ..config import key

class CompanyAssessment(db.Model):
    """ CompanyAssessment Model is used to link companies to their respective assessment """
    __tablename__ = "company_assessment"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessment.id'))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
