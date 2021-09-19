from .. import db, flask_bcrypt
import datetime
import jwt
from app.main.model.blacklist import BlacklistToken
from ..config import key

class UserTeam(db.Model):
    """UserTeam Model is used to link users within a team"""
    __tablename__ = "user_team"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    role=db.Column(db.String(50), unique=False, nullable=False, default='Viewer')
    created_by=db.Column(db.Integer, db.ForeignKey('user.id'))
    modified_by=db.Column(db.Integer, db.ForeignKey('user.id'))
    created_time=db.Column(db.DateTime, unique=False, nullable=False)
    modified_time=db.Column(db.DateTime, unique=False, nullable=False)
    is_deleted=db.Column(db.Boolean, unique=False, nullable=False)
    is_active=db.Column(db.Boolean, unique=False, nullable=False)
    #ROLE IS OWNER, EDITOR, VIEWER