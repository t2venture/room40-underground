from flask import request
from flask_restplus import Resource, reqparse

from ..util.dto import TeamDto
from ..service.team_service import save_new_team, get_all_teams, get_a_team, update_team, delete_a_team
from ..service.user_team_service import check_user_in_team, check_user_is_owner_or_editor, check_user_is_owner
from ..service.auth_helper import Auth
from ..util.decorator import token_required, admin_token_required
import datetime
api = TeamDto.api
_team = TeamDto.team


@api.route('/')
class TeamList(Resource):
    @api.doc('list_of_teams for a team')
    @api.param('user_id', 'user to search for teams for')
    @api.param('portfolio_id', 'portfolio to search for teams')
    @api.param('is_active', 'whether the team is active')
    @api.param('is_deleted', 'whether the team is deleted')
    @api.marshal_list_with(_team, envelope='data')
    @token_required
    def get(self):
        """List all teams"""
        parser = reqparse.RequestParser()
        parser.add_argument("user_id", type=int)
        parser.add_argument("portfolio_id", type=int)
        parser.add_argument("is_active", type=bool)
        parser.add_argument("is_deleted", type=bool)
        args = parser.parse_args()
        logined, status = Auth.get_logged_in_user(request)
        token=logined.get('data')
        if not token:
            return logined, status
        if token['admin']==False:
            args["user_id"]=token["user_id"]
        else:
            args['user_id']=1
        return get_all_teams(args["user_id"], args["portfolio_id"], args["is_active"], args["is_deleted"])

    @api.response(201, 'Team successfully created.')
    @api.doc('create a new team')
    @api.expect(_team, validate=True)
    @token_required
    def post(self):
        """Creates a new Team """
        data = request.json
        logined, status = Auth.get_logged_in_user(request)
        token=logined.get('data')
        if not token:
            return logined, status
        login_user={"login_user_id": token['user_id']}
        action_time={"action_time": datetime.datetime.utcnow()}
        data.update(login_user)
        data.update(action_time)
        return save_new_team(data=data)

@api.route('/<team_id>')
@api.param('team_id', 'The Team identifier')
@api.response(404, 'Team not found.')
class Team(Resource):
    @api.doc('get a team')
    @api.marshal_with(_team)
    @token_required
    def get(self, team_id):
        """get a team given its identifier"""
        team = get_a_team(team_id)
        logined, status = Auth.get_logged_in_user(request)
        token=logined.get('data')
        if not token:
            return logined, status
        if token['admin']==False:
            if check_user_in_team(token['user_id'], team_id)==False:
                response_object = {
                'status': 'fail',
                'message': 'You cannot view this information.'
                }
                return response_object, 401
        if not team:
            api.abort(404)
        else:
            return team

    @api.response(201, 'team successfully created.')
    @api.doc('update a team')
    @api.expect(_team, validate=True)
    @token_required
    def put(self, team_id):
        """Update a team """
        data = request.json
        logined, status = Auth.get_logged_in_user(request)
        token=logined.get('data')
        if not token:
            return logined, status
        if token['admin']==False:
            if check_user_in_team(token['user_id'], team_id)==False:
                response_object = {
                'status': 'fail',
                'message': 'You cannot update this information. You need to be a teammember.'
                }
                return response_object, 401
            if check_user_is_owner_or_editor(token['user_id'], team_id)==False:
                response_object = {
                'status': 'fail',
                'message': 'You cannot update this information. You need to be a owner or editor.'
                }
                return response_object, 401
        login_user={"login_user_id": token['user_id']}
        action_time={"action_time": datetime.datetime.utcnow()}
        data.update(login_user)
        data.update(action_time) 
        return update_team(team_id, data)

    @api.response(201, 'team successfully deleted.')
    @api.doc('delete a team')
    @token_required
    def delete(self, team_id):
        """Delete a team """
        logined, status = Auth.get_logged_in_user(request)
        token=logined.get('data')
        if not token:
            return logined, status
        if token['admin']==False:
            if check_user_in_team(token['user_id'], team_id)==False:
                response_object = {
                'status': 'fail',
                'message': 'You cannot delete this information.'
                }
                return response_object, 401
            if check_user_is_owner(token['user_id'], team_id)==False:
                response_object = {
                'status': 'fail',
                'message': 'You cannot delete this information.'
                }
                return response_object, 401
        data=dict()
        login_user={"login_user_id": token['user_id']}
        action_time={"action_time": datetime.datetime.utcnow()}
        data.update(login_user)
        data.update(action_time) 
        return delete_a_team(team_id, data)