from flask import request
from flask_restplus import Resource, reqparse

from ..util.dto import UserTeamDto
from ..service.user_team_service import save_new_user_team, get_all_user_teams, get_a_user_team, update_user_team, delete_a_user_team
from ..service.auth_helper import Auth
from ..util.decorator import token_required, admin_token_required
from ..service.user_team_service import check_user_in_team, check_user_is_owner_or_editor, check_user_is_owner
import datetime
api = UserTeamDto.api
_user_team = UserTeamDto.user_team


@api.route('/')
class UserTeamList(Resource):
    @api.doc('list_of_user_teams')
    @api.marshal_list_with(_user_team, envelope='data')
    @api.param('is_active', 'whether the user_team is active')
    @api.param('is_deleted', 'whether the user_team is deleted')
    @token_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("is_active", type=bool)
        parser.add_argument("is_deleted", type=bool)
        args = parser.parse_args()
        logined, status = Auth.get_logged_in_user(request)
        token=logined.get('data')
        if not token:
            return logined, status
        if token['admin']==False:
            usr=token["user_id"]
        else:
            usr=1
        return get_all_user_teams(args["is_active"], args["is_deleted"], usr)

    @api.response(201, 'user_team successfully created.')
    @api.doc('create a new user_team')
    @api.expect(_user_team, validate=True)
    @token_required
    def post(self):
        """Creates a new user_team"""
        data = request.json
        logined, status = Auth.get_logged_in_user(request)
        token=logined.get('data')
        if not token:
            return logined, status
        if token['admin']==False:
            if check_user_in_team(token['user_id'], data['team_id'])==False:
                response_object = {
                'status': 'fail',
                'message': 'You cannot add this information.'
                }
                return response_object, 401
            if check_user_is_owner(token['user_id'], data['team_id'])==False:
                response_object = {
                'status': 'fail',
                'message': 'You cannot add this information.'
                }
                return response_object, 401
        login_user={"login_user_id": token['user_id']}
        action_time={"action_time": datetime.datetime.utcnow()}
        data.update(login_user)
        data.update(action_time)   
        return save_new_user_team(data=data)

@api.route('/<user_team_id>')
@api.param('user_team_id', 'The user_team identifier')
@api.response(404, 'user_team not found.')
class UserTeam(Resource):
    @api.doc('get a user_team')
    @api.marshal_with(_user_team)
    @token_required
    def get(self, user_team_id):
        """get a user_team given its identifier"""
        logined, status = Auth.get_logged_in_user(request)
        token=logined.get('data')
        if not token:
            return logined, status
        if token['admin']==False:
            usr=token["user_id"]
        user_team = get_a_user_team(user_team_id)
        tm=user_team["team_id"]
        if check_user_in_team(usr, tm)==False:
            response_object = {
                'status': 'fail',
                'message': 'You cannot view this information.'
                }
            return response_object, 401
        if not user_team:
            api.abort(404)
        else:
            return user_team

    @api.response(201, 'user_team successfully created.')
    @api.doc('update a user_team')
    @api.expect(_user_team, validate=True)
    @token_required
    def put(self, user_team_id):
        """Update a user_team """
        data = request.json
        logined, status = Auth.get_logged_in_user(request)
        token=logined.get('data')
        if not token:
            return logined, status
        if token['admin']==False:
            usr=token["user_id"]
        user_team = get_a_user_team(user_team_id)
        tm=user_team["team_id"]
        if check_user_in_team(usr, tm)==False:
            response_object = {
                'status': 'fail',
                'message': 'You cannot update this information.'
                }
            return response_object, 401
        if check_user_is_owner(usr, tm)==False:
            response_object = {
                'status': 'fail',
                'message': 'You cannot update this information.'
                }
            return response_object, 401
        login_user={"login_user_id": token['user_id']}
        action_time={"action_time": datetime.datetime.utcnow()}
        data.update(login_user)
        data.update(action_time)   
        return update_user_team(user_team_id, data)

    @api.response(201, 'user_team successfully deleted.')
    @api.doc('delete a user_team')
    @token_required
    def delete(self, user_team_id):
        """Delete a user_team """
        logined, status = Auth.get_logged_in_user(request)
        token=logined.get('data')
        if not token:
            return logined, status
        if token['admin']==False:
            usr=token["user_id"]
        user_team = get_a_user_team(user_team_id)
        tm=user_team["team_id"]
        if check_user_in_team(usr, tm)==False:
            response_object = {
                'status': 'fail',
                'message': 'You cannot update this information.'
                }
            return response_object, 401
        if check_user_is_owner_or_editor(usr, tm)==False:
            response_object = {
                'status': 'fail',
                'message': 'You cannot update this information.'
                }
            return response_object, 401
        data=dict()
        login_user={"login_user_id": token['user_id']}
        action_time={"action_time": datetime.datetime.utcnow()}
        data.update(login_user)
        data.update(action_time)    
        return delete_a_user_team(user_team_id, data)