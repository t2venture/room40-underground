from flask import request
from flask_restplus import Resource

from ..util.dto import HouseUnitDto
from ..service.house_unit_service import save_new_house_unit, get_all_house_units, get_a_house_unit, update_house_unit, delete_a_house_unit

api = HouseUnitDto.api
_house_unit = HouseUnitDto.house_unit


@api.route('/')
class HouseUnitList(Resource):
    @api.doc('list_of_house_units for a house_unit')
    @api.marshal_list_with(_house_unit, envelope='data')
    def get(self):
        """List all house_units"""
        return get_all_house_units()

    @api.response(201, 'house_unit successfully created.')
    @api.doc('create a new house_unit')
    @api.expect(_house_unit, validate=True)
    def post(self):
        """Creates a new house_unit """
        data = request.json
        return save_new_house_unit(data=data)

@api.route('/<house_unit_id>')
@api.param('house_unit_id', 'The house_unit identifier')
@api.response(404, 'house_unit not found.')
class HouseUnit(Resource):
    @api.doc('get a house_unit')
    @api.marshal_with(_house_unit)
    def get(self, house_unit_id):
        """get a house_unit given its identifier"""
        house_unit = get_a_house_unit(house_unit_id)
        if not house_unit:
            api.abort(404)
        else:
            return house_unit

    @api.response(201, 'house_unit successfully created.')
    @api.doc('update a house_unit')
    @api.expect(_house_unit, validate=True)
    def put(self, house_unit_id):
        """Update a house_unit """
        data = request.json
        return update_house_unit(house_unit_id, data)

    @api.response(201, 'house_unit successfully deleted.')
    @api.doc('delete a house_unit')
    def delete(self, house_unit_id):
        """Delete a house_unit """
        return delete_a_house_unit(house_unit_id)