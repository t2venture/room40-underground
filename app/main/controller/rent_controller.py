from flask import request
from flask_restplus import Resource

from ..util.dto import RentDto
from ..service.rent_service import save_new_rent, get_all_rents, get_a_rent, update_rent, delete_a_rent

api = RentDto.api
_rent = RentDto.rent


@api.route('/')
class RentList(Resource):
    @api.doc('list_of_rents for a rent')
    @api.marshal_list_with(_rent, envelope='data')
    def get(self):
        """List all rents"""
        return get_all_rents()

    @api.response(201, 'rent successfully created.')
    @api.doc('create a new rent')
    @api.expect(_rent, validate=True)
    def post(self):
        """Creates a new rent"""
        data = request.json
        return save_new_rent(data=data)

@api.route('/<rent_id>')
@api.param('rent_id', 'The rent identifier')
@api.response(404, 'rent not found.')
class Rent(Resource):
    @api.doc('get a rent')
    @api.marshal_with(_rent)
    def get(self, rent_id):
        """get a rent given its identifier"""
        rent = get_a_rent(rent_id)
        if not rent:
            api.abort(404)
        else:
            return rent

    @api.response(201, 'rent successfully created.')
    @api.doc('update a rent')
    @api.expect(_rent, validate=True)
    def put(self, rent_id):
        """Update a rent """
        data = request.json
        return update_rent(rent_id, data)

    @api.response(201, 'rent successfully deleted.')
    @api.doc('delete a rent_model')
    def delete(self, rent_id):
        """Delete a rent"""
        return delete_a_rent(rent_id)