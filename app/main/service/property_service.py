import uuid
import datetime

from app.main import db
from app.main.model.property import Property
from app.main.model.property_model import PropertyModel
from app.main.model.property_history import PropertyHistory
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
            photos=data['photos'],
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

        property.majorcity=data['majorcity']
        property.address=data['address']
        property.building_sqft_area=data['building_sqft_area']
        property.gross_sqft_area=data['gross_sqft_area']
        property.latitude=data['latitude']
        property.longitude=data['longitude']
        property.street=data['street']
        property.housenumber=data['housenumber']
        property.state=data['state']
        property.fips_code=data['fips_code']
        property.usage_code=data['usage_code']
        property.bd_rms=data['bd_rms']
        property.bt_rms=data['bt_rms']
        property.zipcode=data['zipcode']
        property.photos=data['photos']
        property.market_price=data['market_price']
        property.listed=data['listed']
        property.cherre_id=data['cherre_id']
        property.ann_mortgage_cost=data['ann_mortgage_cost']
        property.estimated_rent=data['estimated_rent']
        property.cap_rate=data['cap_rate']
        property.yield_rate=data['yield_rate']
        property.lasso_score=data['lasso_score']
        property.lasso_property=data['lasso_property']
        property.lasso_economics=data['lasso_economics']
        property.lasso_location=data['lasso_location']
        property.lasso_macro=data['lasso_macro']
        property.hoa_fee=data['hoa_fee']
        property.hoa_rent=data['hoa_rent']
        property.est_property_tax=data['est_property_tax']
        property.est_insurance=data['est_insurance']
        property.is_active=data['is_active']
        property.modified_time=data['action_time']
        property.modified_by=data['login_user']
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

def delete_a_property(property_id, data):
    try:
        del_propertys=Property.query.filter_by(id=property_id).all()
        for dp in del_propertys:
            dp.is_deleted=True
            dp.modified_by=data['login_user_id'],
            dp.modified_time=data['action_time']
        db.session.commit()

        del_pms=PropertyModel.query.filter_by(property_id=property_id).all()

        for dpm in del_pms:
            dpm.is_deleted=True
            dpm.modified_time=data['action_time']
            dpm.modified_by=data['login_user_id']
            #should be 1
        db.session.commit()

        del_phs=PropertyHistory.query.filter_by(property_id=property_id).all()

        for dhs in del_phs:
            dhs.is_deleted=True
            dhs.modified_time=data['action_time']
            dhs.modified_by=data['login_user_id']
            #should be 1
        db.session.commit()


        dppfs=PropertyPortfolio.query.filter_by(property_id=property_id).delete()
        for ppf in dppfs:
            ppf.is_deleted=True
            ppf.modified_time=data["action_time"]
            ppf.modified_by=data["login_user_id"]
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

def get_all_propertys(is_deleted=False, is_active=True, portfolio_id="", address="", street="", housenumber="", min_area=0, max_area=999999, north=89.99, south=-89.99, east=179.99, west=-179.99, min_lasso_score=0, max_lasso_score=100, min_price=0, max_price=9999999, bds="", bths=""):
    propertys=Property.query.filter_by(is_deleted=False, is_active=True)
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
        propertys=propertys.filter(Property.building_sqft_area>=min_area)
    if max_area and max_area<999999:
        propertys=propertys.filter(Property.building_sqft_area<=max_area)
    if north and north!=89.99:
        propertys=propertys.filter(Property.latitude<=north)
    if south and south!=-89.99:
        propertys=propertys.filter(Property.latitude>=south)
    if east and east!=179.99:
        propertys=propertys.filter(Property.longitude<=east)
    if west and west!=-179.99:
        propertys=propertys.filter(Property.longitude>=west)
    if min_lasso_score and min_lasso_score!=0:
        propertys=propertys.filter(Property.lasso_score>=min_lasso_score)
    if max_lasso_score and max_lasso_score!=100:
        propertys=propertys.filter(Property.lasso_score<=max_lasso_score)
    if min_price and min_price!=0:
        propertys=propertys.filter(Property.market_price>=min_price)
    if max_price and max_price!=9999999:
        propertys=propertys.filter(Property.market_price<=max_price)
    if bds and bds!="":
        bdlist = [int(x.strip()) for x in bds.split(',') if x.strip().isdigit()]
        for b in bdlist:
            propertys=propertys.filter(Property.bd_rms==b)
    if bths and bths!="":
        bthlist=[int(x.strip()) for x in bths.split(',') if x.strip().isdigit()]
        for bt in bthlist:
            propertys=propertys.filter(Property.bt_rms==bt)
    return propertys.all()

def get_a_property(property_id):
    return Property.query.filter_by(id=property_id).filter_by(is_deleted=False).filter_by(is_active=True).first()

def get_all_deleted_propertys(property_id):
    propertys=Property.query.filter_by(is_deleted=True)
    return propertys.all()

def get_a_deleted_property(property_id):
    return Property.query.filter_by(id=property_id).filter_by(is_deleted=True).all()

def save_changes(data):
    db.session.add(data)
    db.session.commit()
