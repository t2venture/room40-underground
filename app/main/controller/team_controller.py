from flask import request
from flask_restplus import Resource, reqparse

from ..util.dto import TeamDto
from ..service.team_service import save_new_team, get_all_teams, get_a_team, update_team, delete_a_team

api = TeamDto.api
_team = TeamDto.team


@api.route('/')
class TeamList(Resource):
    @api.doc('list_of_teams for a team')
    @api.param('user_id', 'user to search for teams for')
    @api.param('portfolio_id', 'portfolio to search for teams')
    @api.marshal_list_with(_team, envelope='data')
    def get(self):
        """List all teams"""
        parser = reqparse.RequestParser()
        parser.add_argument("user_id", type=int)
        parser.add_argument("portfolio_id", type=int)
        args = parser.parse_args()
        return get_all_teams(args["user_id"], args["portfolio_id"])

    @api.response(201, 'Team successfully created.')
    @api.doc('create a new team')
    @api.expect(_team, validate=True)
    def post(self):
        """Creates a new Team """
        data = request.json
        return save_new_team(data=data)

@api.route('/<team_id>')
@api.param('team_id', 'The Team identifier')
@api.response(404, 'Team not found.')
class Team(Resource):
    @api.doc('get a team')
    @api.marshal_with(_team)
    def get(self, team_id):
        """get a team given its identifier"""
        team = get_a_team(team_id)
        if not team:
            api.abort(404)
        else:
            return team

    @api.response(201, 'team successfully created.')
    @api.doc('update a team')
    @api.expect(_team, validate=True)
    def put(self, team_id):
        """Update a team """
        data = request.json
        return update_team(team_id, data)

    @api.response(201, 'team successfully deleted.')
    @api.doc('delete a team')
    def delete(self, team_id):
        """Delete a team """
        return delete_a_team(team_id)