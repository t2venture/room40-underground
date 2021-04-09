from .. import db, flask_bcrypt
import datetime
import jwt
from app.main.model.blacklist import BlacklistToken
from ..config import key

class DealNote(db.Model):
    """DealNote Model is used to link deals to their respective note"""
    __tablename__ = "deal_note"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    deal_id = db.Column(db.Integer, db.ForeignKey('deal.id'))
    note_id = db.Column(db.Integer, db.ForeignKey('note.id'))
