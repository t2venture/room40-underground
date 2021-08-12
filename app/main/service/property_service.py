import uuid
import datetime

from app.main import db
from app.main.model.property import Property
from app.main.model.property_portfolio import PropertyPortfolio
from app.main.service.property_portfolio_service import get_propertys_from_portfolio
from app.main.util.scrape_property import strip_housenumber_street

def save_new_property(data):
    try:
        if not data['street'] or not data['housenumber']:
            data['street']=strip_housenumber_street(data['address'])[1]
            data['housenumber']=strip_housenumber_street(data['address'])[0]
        new_property = Property(
            majorcity=data['majorcity'],
            address=data['address'],
            building_sqft_area=data['building_sqft_area'],
            gross_sqft_area=data['gross_sqft_area'],
            latitude=data['latitude'],
            longitude=data['longitude'],
            street=data['street'],
            housenumber=data['housenumber'],
        )
        save_changes(new_property)
        response_object = {
                'status': 'success',
                'message': 'Successfully registered.',
            }
        return response_object, 201

    except Exception as e:
        print(e)
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401

def update_property(property_id, data):

    try:
        property = get_a_property(property_id)

        property.majorcity=data['majorcity'],
        property.address=data['address'],
        property.building_sqft_area=data['building_sqft_area'],
        property.gross_sqft_area=data['gross_sqft_area'],
        property.latitude=data['latitude'],
        property.longitude=data['longitude'],
        property.street=data['street'],
        property.housenumber=data['housenumber']
        save_changes(property)

        response_object = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                }
        return response_object, 201

    except Exception as e:
        print(e)
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401

def delete_a_property(property_id):
    try:
        Property.query.filter_by(id=property_id).delete()
        db.session.commit()
        PropertyPortfolio.query.filter_by(property_id=property_id).delete()
        db.session.commit()
        response_object = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                }
        return response_object, 201

    except Exception as e:
        print(e)
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401

def get_all_propertys(portfolio_id="", address="", street="", housenumber=""):
    propertys=Property.query
    if portfolio_id and portfolio_id!="":
        property_ids=[pt.property_id for pt in get_propertys_from_portfolio(portfolio_id)]
        propertys=propertys.filter(Property.id.in_(property_ids))
    if address and address!="":
        propertys=propertys.filter(Property.address.like(address))
    if street and street!="":
        propertys=propertys.filter(Property.street.like(street))
    if housenumber and housenumber!="":
        propertys=propertys.filter(Property.housenumber.like(housenumber))
    return propertys.all()


def get_a_property(property_id):
    return Property.query.filter_by(id=property_id).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()
