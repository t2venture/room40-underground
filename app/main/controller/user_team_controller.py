from flask import request
from flask_restplus import Resource

from ..util.dto import UserTeamDto
from ..service.user_team_service import save_new_user_team, get_all_user_teams, get_a_user_team, update_user_team, delete_a_user_team

api = UserTeamDto.api
_user_team = UserTeamDto.user_team


@api.route('/')
class UserTeamList(Resource):
    @api.doc('list_of_user_teams')
    @api.marshal_list_with(_user_team, envelope='data')
    def get(self):
        """List all user_teams"""
        return get_all_user_teams()

    @api.response(201, 'user_team successfully created.')
    @api.doc('create a new user_team')
    @api.expect(_user_team, validate=True)
    def post(self):
        """Creates a new user_team """
        data = request.json
        return save_new_user_team(data=data)

@api.route('/<user_team_id>')
@api.param('user_team_id', 'The user_team identifier')
@api.response(404, 'user_team not found.')
class UserTeam(Resource):
    @api.doc('get a user_team')
    @api.marshal_with(_user_team)
    def get(self, user_team_id):
        """get a user_team given its identifier"""
        user_team = get_a_user_team(user_team_id)
        if not user_team:
            api.abort(404)
        else:
            return user_team

    @api.response(201, 'user_team successfully created.')
    @api.doc('update a user_team')
    @api.expect(_user_team, validate=True)
    def put(self, user_team_id):
        """Update a user_team """
        data = request.json
        return update_user_team(user_team_id, data)

    @api.response(201, 'user_team successfully deleted.')
    @api.doc('delete a user_team')
    def delete(self, user_team_id):
        """Delete a user_team """
        return delete_a_user_team(user_team_id)