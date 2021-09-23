from flask import request
from flask_restplus import Resource, reqparse
from flask_restplus.fields import String
from ..util.decorator import token_required, admin_token_required
from ..util.dto import PropertyDto
from ..service.property_service import save_new_property, get_all_propertys, get_a_property, update_property, delete_a_property
from ..service.auth_helper import Auth
import datetime
api = PropertyDto.api
_property = PropertyDto.property


@api.route('/')
class PropertyList(Resource):
    @api.doc('list_of_propertys for a property')
    @api.param('is_deleted', 'whether the property is deleted or not')
    @api.param('is_active', 'whether the property is active or not')
    @api.param('portfolio_id', 'portfolio id to search properties in')
    @api.param('address', 'address to search properties for')
    @api.param('street', 'street to search properties for')
    @api.param('house_number', 'house number to search properties for')
    @api.param('min_area', 'minimum area of the property')
    @api.param('max_area', 'maximum area of the property')
    @api.param('north', 'northernmost latitude to search in')
    @api.param('south', 'southernmost latitude to search in')
    @api.param('east', 'easternmost longitude to search in')
    @api.param('west', 'westernmost longitude to search in')
    @api.param('min_lasso_score', 'minimum lasso score')
    @api.param('max_lasso_score', 'maximum lasso score')
    @api.param('min_price', 'minimum price')
    @api.param('max_price', 'maximum price')
    @api.param('bds', 'possible bedroom counts, comma separated')
    @api.param('bths', 'possible bathroom counts, comma separated')
    @api.marshal_list_with(_property, envelope='data')
    @token_required
    def get(self):
        """List all propertys"""
        parser = reqparse.RequestParser()
        parser.add_argument("is_deleted", type=bool)
        parser.add_argument("is_active", type=bool)
        parser.add_argument("portfolio_id", type=int)
        parser.add_argument("address", type=str)
        parser.add_argument("street", type=str)
        parser.add_argument("housenumber", type=str)
        parser.add_argument("min_area", type=int)
        parser.add_argument("max_area", type=int)
        parser.add_argument("north", type=float)
        parser.add_argument("south", type=float)
        parser.add_argument("east", type=float)
        parser.add_argument("west", type=float)
        parser.add_argument('min_lasso_score', type=float)
        parser.add_argument('max_lasso_score', type=float)
        parser.add_argument('min_price', type=int)
        parser.add_argument('max_price', type=int)
        parser.add_argument('bds', type=str)
        parser.add_argument('bths', type=str)
        args = parser.parse_args()
        return get_all_propertys(args['is_deleted'], args['is_active'], args['portfolio_id'], args['address'], args['street'], args['housenumber'], args["min_area"], args["max_area"],
        args['north'], args['south'], args['east'], args['west'], args['min_lasso_score'], args['max_lasso_score'], args['min_price'], args['max_price'],
        args['bds'], args['bths'])

    @api.response(201, 'property successfully created.')
    @api.doc('create a new property')
    @api.expect(_property, validate=True)
    @admin_token_required
    def post(self):
        """Creates a new property """
        data = request.json
        logined, status = Auth.get_logged_in_user(request)
        token=logined.get('data')
        if not token:
            return logined, status
        login_user={"login_user_id": token['user_id']}
        action_time={"action_time": datetime.datetime.utcnow()}
        data.update(login_user)
        data.update(action_time)	  
        return save_new_property(data=data)

@api.route('/<property_id>')
@api.param('property_id', 'The property identifier')
@api.response(404, 'property not found.')
class Property(Resource):
    @api.doc('get a Property')
    @api.marshal_with(_property)
    @token_required
    def get(self, property_id):
        """get a property given its identifier"""
        property = get_a_property(property_id)
        if not property:
            api.abort(404)
        else:
            return property

    @api.response(201, 'property successfully created.')
    @api.doc('update a property')
    @api.expect(_property, validate=True)
    @admin_token_required
    def put(self, property_id):
        """Update a property """
        data = request.json
        logined, status = Auth.get_logged_in_user(request)
        token=logined.get('data')
        if not token:
            return logined, status
        login_user={"login_user_id": token['user_id']}
        action_time={"action_time": datetime.datetime.utcnow()}
        data.update(login_user)
        data.update(action_time)	
        return update_property(property_id, data)

    @api.response(201, 'property successfully deleted.')
    @api.doc('delete a property')
    @admin_token_required
    def delete(self, property_id):
        """Delete a property """
        logined, status = Auth.get_logged_in_user(request)
        token=logined.get('data')
        if not token:
            return logined, status
        data=dict()
        login_user={"login_user_id": token['user_id']}
        action_time={"action_time": datetime.datetime.utcnow()}
        data.update(login_user)
        data.update(action_time)	
        return delete_a_property(property_id, data)