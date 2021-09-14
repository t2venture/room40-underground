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
            state=data['state'],
            fips_code=data['fips_code'],
            usage_code=data['usage_code'],
            bd_rms=data['bd_rms'],
            bt_rms=data['bt_rms'],
            ###FROM HERE
            zipcode=data['zipcode'],
            market_price=data['market_price'],
            listed=data['listed'],
            cherre_id=data['cherre_id'],
            ann_mortgage_cost=data['ann_mortgage_cost'],
            estimated_rent=data['estimated_rent'],
            cap_rate=data['cap_rate'],
            yield_rate=data['yield_rate'],
            lasso_score=data['lasso_score'],
            lasso_property=data['lasso_property'],
            lasso_economics=data['lasso_economics'],
            lasso_location=data['lasso_location'],
            lasso_macro=data['lasso_macro'],
            hoa_fee=data['hoa_fee'],
            hoa_rent=data['hoa_rent'],
            est_property_tax=data['est_property_tax'],
            est_insurance=data['est_insurance'],
            is_deleted=False,
            is_active=True,
            created_time=data['action_time'],
            modified_time=data['action_time'],
            modified_by=1,
            created_by=1,
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
        property.state=data['state'],
        property.fips_code=data['fips_code'],
        property.usage_code=data['usage_code'],
        property.bd_rms=data['bd_rms'],
        property.bt_rms=data['bt_rms'],
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

def get_all_propertys(portfolio_id="", address="", street="", housenumber="", min_area=0, max_area=999999, north=89.99, south=-89.99, east=179.99, west=-179.99):
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
    if min_area and min_area>0:
        propertys=propertys.filter(Property.building_sqft_area>min_area)
    if max_area and max_area<999999:
        propertys=propertys.filter(Property.building_sqft_area<max_area)
    if north and north!=89.99:
        propertys=propertys.filter(Property.latitude<north)
    if south and south!=-89.99:
        propertys=propertys.filter(Property.latitude>south)
    if east and east!=179.99:
        propertys=propertys.filter(Property.longitude<east)
    if west and west!=-179.99:
        propertys=propertys.filter(Property.longitude>west)
    return propertys.all()

def get_a_property(property_id):
    return Property.query.filter_by(id=property_id).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()
