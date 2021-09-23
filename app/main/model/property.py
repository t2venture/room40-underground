from .. import db, flask_bcrypt
import datetime
import jwt
from app.main.model.blacklist import BlacklistToken
from ..config import key

class Property(db.Model):
    """ Property Model for storing Property related details """
    __tablename__ = "property"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    majorcity=db.Column(db.String(255), unique=False, nullable=False)
    address=db.Column(db.String(255), unique=False, nullable=False)
    state=db.Column(db.String(255), unique=False, nullable=True)
    fips_code=db.Column(db.String(255), unique=False, nullable=True)
    zipcode=db.Column(db.String(255), unique=False, nullable=True)
    usage_code=db.Column(db.String(255), unique=False, nullable=True)
    building_sqft_area=db.Column(db.Integer, unique=False, nullable=True)
    gross_sqft_area=db.Column(db.Integer, unique=False, nullable=True)
    latitude=db.Column(db.Float, unique=False, nullable=False)
    longitude=db.Column(db.Float, unique=False, nullable=False)
    street=db.Column(db.String(255), unique=False, nullable=True)
    housenumber=db.Column(db.String(255), unique=False, nullable=True)
    bd_rms=db.Column(db.String(255), unique=False, nullable=True)
    bt_rms=db.Column(db.String(255), unique=False, nullable=True)
    photos=db.Column(db.String(1011), unique=False, nullable=True)
    market_price=db.Column(db.Integer, unique=False, nullable=True)
    listed=db.Column(db.Boolean, unique=False, nullable=False, default=True)
    cherre_id=db.Column(db.String(255), unique=True, nullable=False)
    #THESE ARE SET TO NULLABLE FOR NOW
    ann_mortgage_cost=db.Column(db.Integer, unique=False, nullable=True)
    estimated_rent=db.Column(db.Integer, unique=False, nullable=True)
    cap_rate=db.Column(db.Float, unique=False, nullable=True)
    yield_rate=db.Column(db.Float, unique=False, nullable=True)
    lasso_score=db.Column(db.Float, unique=False, nullable=True)
    lasso_property=db.Column(db.Float, unique=False, nullable=True)
    lasso_economics=db.Column(db.Float, unique=False, nullable=True)
    lasso_location=db.Column(db.Float, unique=False, nullable=True)
    lasso_macro=db.Column(db.Float, unique=False, nullable=True)
    hoa_fee=db.Column(db.Float, unique=False, nullable=True)
    hoa_rent=db.Column(db.Float, unique=False, nullable=True)
    est_property_tax=db.Column(db.Float, unique=False, nullable=True)
    est_insurance=db.Column(db.Float, unique=False, nullable=True)
    created_by=db.Column(db.Integer, db.ForeignKey('user.id'))
    modified_by=db.Column(db.Integer, db.ForeignKey('user.id'))
    created_time=db.Column(db.DateTime, unique=False, nullable=False)
    modified_time=db.Column(db.DateTime, unique=False, nullable=False)
    is_deleted=db.Column(db.Boolean, unique=False, nullable=False)
    is_active=db.Column(db.Boolean, unique=False, nullable=False)
