from .. import db, flask_bcrypt
import datetime
import jwt
from app.main.model.blacklist import BlacklistToken
from ..config import key

class DealEvent(db.Model):
    """ DealEvent Model is used to link deals to their respective events """
    __tablename__ = "deal_event"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    deal_id = db.Column(db.Integer, db.ForeignKey('deal.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
