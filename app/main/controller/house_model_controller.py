from flask import request
from flask_restplus import Resource

from ..util.dto import HouseModelDto
from ..service.house_model_service import save_new_house_model, get_all_house_models, get_a_house_model, update_house_model, delete_a_house_model

api = HouseModelDto.api
_house_model = HouseModelDto.house_model


@api.route('/')
class HouseModelList(Resource):
    @api.doc('list_of_house_models for a house_model')
    @api.marshal_list_with(_house_model, envelope='data')
    def get(self):
        """List all house_models"""
        return get_all_house_models()

    @api.response(201, 'house_model successfully created.')
    @api.doc('create a new house_model')
    @api.expect(_house_model, validate=True)
    def post(self):
        """Creates a new house_model """
        data = request.json
        return save_new_house_model(data=data)

@api.route('/<house_model_id>')
@api.param('house_model_id', 'The house_model identifier')
@api.response(404, 'house_model not found.')
class HouseModel(Resource):
    @api.doc('get a house_model')
    @api.marshal_with(_house_model)
    def get(self, house_model_id):
        """get a house_model given its identifier"""
        house_model = get_a_house_model(house_model_id)
        if not house_model:
            api.abort(404)
        else:
            return house_model

    @api.response(201, 'house_model successfully created.')
    @api.doc('update a house_model')
    @api.expect(_house_model, validate=True)
    def put(self, house_model_id):
        """Update a house_model """
        data = request.json
        return update_house_model(house_model_id, data)

    @api.response(201, 'house_model successfully deleted.')
    @api.doc('delete a house_model')
    def delete(self, house_model_id):
        """Delete a house_model """
        return delete_a_house_model(house_model_id)