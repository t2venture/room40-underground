from flask import request
from flask_restplus import Resource, reqparse
from ..util.decorator import token_required, admin_token_required
from ..util.dto import PropertyHistoryDto
from ..service.property_history_service import save_new_property_history, get_all_property_historys, get_a_property_history, update_property_history, delete_a_property_history
from ..service.auth_helper import Auth
import datetime
api = PropertyHistoryDto.api
_property_history = PropertyHistoryDto.property_history


@api.route('/')
class PropertyHistoryList(Resource):
    @api.doc('list_of_property_historys for a property_history')
    @api.param('is_deleted', 'whether the property history is deleted or not')
    @api.param('is_active', 'whether the property history is active or not')
    @api.param('property id', 'id of the property the history is for')
    @api.marshal_list_with(_property_history, envelope='data')
    @token_required
    def get(self):
        """List all property_historys"""
        parser = reqparse.RequestParser()
        parser.add_argument("is_deleted", type=bool)
        parser.add_argument("is_active", type=bool)
        parser.add_argument("property_id", type=int)
        args = parser.parse_args()
        return get_all_property_historys(args["is_deleted"], args["is_active"], args["property_id"])

    @api.response(201, 'property_history successfully created.')
    @api.doc('create a new property_history')
    @api.expect(_property_history, validate=True)
    @admin_token_required
    def post(self):
        """Creates a new property_history"""
        data = request.json
        logined, status = Auth.get_logged_in_user(request)
        token=logined.get('data')
        if not token:
            return logined, status
        login_user={"login_user_id": token['user_id']}
        action_time={"action_time": datetime.datetime.utcnow()}
        data.update(login_user)
        data.update(action_time)	 
        return save_new_property_history(data=data)

@api.route('/<property_history_id>')
@api.param('property_history_id', 'The property_history identifier')
@api.response(404, 'property_history not found.')
class PropertyHistopry(Resource):
    @api.doc('get a property_history')
    @api.marshal_with(_property_history)
    @token_required
    def get(self, property_history_id):
        """get a property_history given its identifier"""
        property_history = get_a_property_history(property_history_id)
        if not property_history:
            api.abort(404)
        else:
            return property_history

    @api.response(201, 'property_history successfully created.')
    @api.doc('update a property_history')
    @api.expect(_property_history, validate=True)
    @admin_token_required
    def put(self, property_history_id):
        """Update a property_history """
        data = request.json
        logined, status = Auth.get_logged_in_user(request)
        token=logined.get('data')
        if not token:
            return logined, status
        login_user={"login_user_id": token['user_id']}
        action_time={"action_time": datetime.datetime.utcnow()}
        data.update(login_user)
        data.update(action_time)
        return update_property_history(property_history_id, data)

    @api.response(201, 'property_history successfully deleted.')
    @api.doc('delete a property_history')
    @admin_token_required
    def delete(self, property_history_id):
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
        return delete_a_property_history(property_history_id, data)