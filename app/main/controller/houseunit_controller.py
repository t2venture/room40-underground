from flask import request
from flask_restplus import Resource

from ..util.dto import HouseunitDto
from ..service.houseunit_service import save_new_houseunit, get_all_houseunits, get_a_houseunit, update_houseunit, delete_a_houseunit

api = HouseunitDto.api
_houseunit = HouseunitDto.houseunit


@api.route('/')
class HouseunitList(Resource):
    @api.doc('list_of_houseunits for a houseunit')
    @api.marshal_list_with(_houseunit, envelope='data')
    def get(self):
        """List all houseunits"""
        return get_all_houseunits()

    @api.response(201, 'houseunit successfully created.')
    @api.doc('create a new houseunit')
    @api.expect(_houseunit, validate=True)
    def post(self):
        """Creates a new houseunit """
        data = request.json
        return save_new_houseunit(data=data)

@api.route('/<houseunit_id>')
@api.param('houseunit_id', 'The houseunit identifier')
@api.response(404, 'Houseunit not found.')
class Houseunit(Resource):
    @api.doc('get a houseunit')
    @api.marshal_with(_houseunit)
    def get(self, houseunit_id):
        """get a houseunit given its identifier"""
        houseunit = get_a_houseunit(houseunit_id)
        if not houseunit:
            api.abort(404)
        else:
            return houseunit

    @api.response(201, 'houseunit successfully created.')
    @api.doc('update a houseunit')
    @api.expect(_houseunit, validate=True)
    def put(self, houseunit_id):
        """Update a houseunit """
        data = request.json
        return update_houseunit(houseunit_id, data)

    @api.response(201, 'houseunit successfully deleted.')
    @api.doc('delete a houseunit')
    def delete(self, houseunit_id):
        """Delete a houseunit """
        return delete_a_houseunit(houseunit_id)