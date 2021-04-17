from .. import db, flask_bcrypt
import datetime
import jwt
from app.main.model.blacklist import BlacklistToken
from ..config import key

class Highlight(db.Model):
    """Highlight Model for storing highlights related details """
    __tablename__ = "highlight"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    notes = db.Column(db.String(2000), unique=False, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)