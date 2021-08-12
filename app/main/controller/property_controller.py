from flask import request
from flask_restplus import Resource, reqparse
from flask_restplus.fields import String

from ..util.dto import PropertyDto
from ..service.property_service import save_new_property, get_all_propertys, get_a_property, update_property, delete_a_property

api = PropertyDto.api
_property = PropertyDto.property


@api.route('/')
class PropertyList(Resource):
    @api.doc('list_of_propertys for a property')
    @api.param('portfolio_id', 'portfolio id to search properties in')
    @api.param('address', 'address to search properties for')
    @api.marshal_list_with(_property, envelope='data')
    def get(self):
        """List all propertys"""
        parser = reqparse.RequestParser()
        parser.add_argument("portfolio_id", type=int)
        parser.add_argument("address", type=String)
        args = parser.parse_args()
        return get_all_propertys(args['portfolio_id'], args['address'])

    @api.response(201, 'property successfully created.')
    @api.doc('create a new property')
    @api.expect(_property, validate=True)
    def post(self):
        """Creates a new property """
        data = request.json
        return save_new_property(data=data)

@api.route('/<property_id>')
@api.param('property_id', 'The property identifier')
@api.response(404, 'property not found.')
class Property(Resource):
    @api.doc('get a Property')
    @api.marshal_with(_property)
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
    def put(self, property_id):
        """Update a property """
        data = request.json
        return update_property(property_id, data)

    @api.response(201, 'property successfully deleted.')
    @api.doc('delete a property')
    def delete(self, property_id):
        """Delete a property """
        return delete_a_property(property_id)