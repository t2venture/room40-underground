from .. import db, flask_bcrypt
import datetime
import jwt
from app.main.model.blacklist import BlacklistToken
from ..config import key

class CompanyHighlight(db.Model):
    """ CompanyHighlight Model is used to link companies to their respective highlights """
    __tablename__ = "company_highlight"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    highlight_id = db.Column(db.Integer, db.ForeignKey('highlight.id'))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
