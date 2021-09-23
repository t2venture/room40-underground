from flask import request
from flask_restplus import Resource, reqparse
from ..util.decorator import token_required, admin_token_required
from ..util.dto import PropertyModelDto
from ..service.property_model_service import save_new_property_model, get_all_property_models, get_a_property_model, update_property_model, delete_a_property_model
from ..service.auth_helper import Auth
import datetime
api = PropertyModelDto.api
_property_model = PropertyModelDto.property_model


@api.route('/')
class PropertyModelList(Resource):
    @api.doc('list_of_property_models for a property_model')
    @api.param('is_deleted', 'whether the property model is deleted or not')
    @api.param('is_active', 'whether the property model is active or not')
    @api.param('property id', 'id of the property the model is for')
    @api.marshal_list_with(_property_model, envelope='data')
    @token_required
    def get(self):
        """List all property_models"""
        parser = reqparse.RequestParser()
        parser.add_argument("is_deleted", type=bool)
        parser.add_argument("is_active", type=bool)
        parser.add_argument("property_id", type=int)
        args = parser.parse_args()
        return get_all_property_models(args["is_deleted"], args["is_active"], args["property_id"])

    @api.response(201, 'property_model successfully created.')
    @api.doc('create a new property_model')
    @api.expect(_property_model, validate=True)
    @admin_token_required
    def post(self):
        """Creates a new property_model """
        data = request.json
        logined, status = Auth.get_logged_in_user(request)
        token=logined.get('data')
        if not token:
            return logined, status
        login_user={"login_user_id": token['user_id']}
        action_time={"action_time": datetime.datetime.utcnow()}
        data.update(login_user)
        data.update(action_time)	 
        return save_new_property_model(data=data)

@api.route('/<property_model_id>')
@api.param('property_model_id', 'The property_model identifier')
@api.response(404, 'property_model not found.')
class PropertyModel(Resource):
    @api.doc('get a property_model')
    @api.marshal_with(_property_model)
    @token_required
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
    @admin_token_required
    def put(self, property_model_id):
        """Update a property_model """
        data = request.json
        logined, status = Auth.get_logged_in_user(request)
        token=logined.get('data')
        if not token:
            return logined, status
        login_user={"login_user_id": token['user_id']}
        action_time={"action_time": datetime.datetime.utcnow()}
        data.update(login_user)
        data.update(action_time)
        return update_property_model(property_model_id, data)

    @api.response(201, 'property_model successfully deleted.')
    @api.doc('delete a property_model')
    @admin_token_required
    def delete(self, property_model_id):
        """Delete a property"""
        logined, status = Auth.get_logged_in_user(request)
        token=logined.get('data')
        if not token:
            return logined, status
        data=dict()
        login_user={"login_user_id": token['user_id']}
        action_time={"action_time": datetime.datetime.utcnow()}
        data.update(login_user)
        data.update(action_time)	
        return delete_a_property_model(property_model_id, data)