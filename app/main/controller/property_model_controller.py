from flask import request
from flask_restplus import Resource

from ..util.dto import PropertyModelDto
from ..service.property_model_service import save_new_property_model, get_all_property_models, get_a_property_model, update_property_model, delete_a_property_model

api = PropertyModelDto.api
_property_model = PropertyModelDto.property_model


@api.route('/')
class PropertyModelList(Resource):
    @api.doc('list_of_property_models for a property_model')
    @api.marshal_list_with(_property_model, envelope='data')
    def get(self):
        """List all property_models"""
        return get_all_property_models()

    @api.response(201, 'property_model successfully created.')
    @api.doc('create a new property_model')
    @api.expect(_property_model, validate=True)
    def post(self):
        """Creates a new property_model """
        data = request.json
        return save_new_property_model(data=data)

@api.route('/<property_model_id>')
@api.param('property_model_id', 'The property_model identifier')
@api.response(404, 'property_model not found.')
class PropertyModel(Resource):
    @api.doc('get a property_model')
    @api.marshal_with(_property_model)
    def get(self, property_model_id):
        """get a property_model given its identifier"""
        property_model = get_a_property_model(property_model_id)
        if not property_model:
            api.abort(404)
        else:
            return property_model

    @api.response(201, 'property_model successfully created.')
    @api.doc('update a property_model')
    @api.expect(_property_model, validate=True)
    def put(self, property_model_id):
        """Update a property_model """
        data = request.json
        return update_property_model(property_model_id, data)

    @api.response(201, 'property_model successfully deleted.')
    @api.doc('delete a property_model')
    def delete(self, property_model_id):
        """Delete a property"""
        return delete_a_property_model(property_model_id)