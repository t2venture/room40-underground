from .. import db, flask_bcrypt
import datetime
import jwt
from app.main.model.blacklist import BlacklistToken
from ..config import key

def same_as(column_name):
    def default_function(context):
        return context.current_parameters.get(column_name)
    return default_function

class User(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name=db.Column(db.String(255), unique=False, nullable=False)
    last_name=db.Column(db.String(255), unique=False, nullable=False)
    profile_url=db.Column(db.String(511), unique=False, nullable=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    public_id = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(100))
    linkedin_url = db.Column(db.String(255), unique=False, nullable=True)
    twitter_url = db.Column(db.String(255), unique=False, nullable=True)
    phonenumber = db.Column(db.String(30), unique=False, nullable=True)
    company_name=db.Column(db.String(255), unique=False, default="Independent")
    created_by=db.Column(db.Integer, unique=False, nullable=False, default=same_as('id'))
    modified_by=db.Column(db.Integer, unique=False, nullable=False, default=same_as('id'))
    created_time=db.Column(db.DateTime, unique=False, nullable=False)
    modified_time=db.Column(db.DateTime, unique=False, nullable=False)
    is_deleted=db.Column(db.Boolean, unique=False, nullable=False, default=False)
    is_active=db.Column(db.Boolean, unique=False, nullable=False, default=True)
    confirmed=db.Column(db.Boolean, unique=False, nullable=False, default=False)
    confirmed_on=db.Column(db.DateTime, unique=False, nullable=True)


    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User '{}'>".format(self.username)

    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                key,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod  
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, key, algorithms="HS256")
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'