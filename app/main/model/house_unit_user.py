from .. import db, flask_bcrypt
import datetime
import jwt
from app.main.model.blacklist import BlacklistToken
from ..config import key

class HouseUnitUser(db.Model):
	"HouseUnitUser is used to link houseunits to portfolios in a many to many relation"
	__tablename__="house_unit_user"

	id=db.Column(db.Integer, primary_key=True, autoincrement=True)
	house_unit_id=db.Column(db.Integer, db.ForeignKey('house_unit.id'))
	user_id=db.Column(db.Integer, db.ForeignKey('user.id'))
	