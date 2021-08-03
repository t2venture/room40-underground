from flask import request
from flask_restplus import Resource

from ..util.dto import HousemodelDto
from ..service.housemodel_service import save_new_housemodel, get_all_housemodels, get_a_housemodel, update_housemodel, delete_a_housemodel

api = HousemodelDto.api
_housemodel = HousemodelDto.housemodel


@api.route('/')
class HousemodelList(Resource):
    @api.doc('list_of_housemodels for a housemodel')
    @api.marshal_list_with(_housemodel, envelope='data')
    def get(self):
        """List all housemodels"""
        return get_all_housemodels()

    @api.response(201, 'housemodel successfully created.')
    @api.doc('create a new housemodel')
    @api.expect(_housemodel, validate=True)
    def post(self):
        """Creates a new housemodel """
        data = request.json
        return save_new_housemodel(data=data)

@api.route('/<housemodel_id>')
@api.param('housemodel_id', 'The housemodel identifier')
@api.response(404, 'Housemodel not found.')
class Housemodel(Resource):
    @api.doc('get a housemodel')
    @api.marshal_with(_housemodel)
    def get(self, housemodel_id):
        """get a housemodel given its identifier"""
        housemodel = get_a_housemodel(housemodel_id)
        if not housemodel:
            api.abort(404)
        else:
            return housemodel

    @api.response(201, 'housemodel successfully created.')
    @api.doc('update a housemodel')
    @api.expect(_housemodel, validate=True)
    def put(self, housemodel_id):
        """Update a housemodel """
        data = request.json
        return update_housemodel(housemodel_id, data)

    @api.response(201, 'housemodel successfully deleted.')
    @api.doc('delete a housemodel')
    def delete(self, housemodel_id):
        """Delete a housemodel """
        return delete_a_housemodel(housemodel_id)