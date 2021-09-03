from flask import request
from flask_restplus import Resource

from ..util.dto import TeamPortfolioDto
from ..service.team_portfolio_service import save_new_team_portfolio, get_all_team_portfolios, get_a_team_portfolio, update_team_portfolio, delete_a_team_portfolio

api = TeamPortfolioDto.api
_team_portfolio = TeamPortfolioDto.team_portfolio


@api.route('/')
class TeamPortfolioList(Resource):
    @api.doc('list_of_team_portfolios for a team_portfolio')
    @api.marshal_list_with(_team_portfolio, envelope='data')
    def get(self):
        """List all team_portfolios"""
        return get_all_team_portfolios()

    @api.response(201, 'team_portfolio successfully created.')
    @api.doc('create a new team_portfolio')
    @api.expect(_team_portfolio, validate=True)
    def post(self):
        """Creates a new team_portfolio """
        data = request.json
        return save_new_team_portfolio(data=data)

@api.route('/<team_portfolio_id>')
@api.param('team_portfolio_id', 'The team_portfolio identifier')
@api.response(404, 'team_portfolio not found.')
class TeamPortfolio(Resource):
    @api.doc('get a team_portfolio')
    @api.marshal_with(_team_portfolio)
    def get(self, team_portfolio_id):
        """get a team_portfolio given its identifier"""
        team_portfolio = get_a_team_portfolio(team_portfolio_id)
        if not team_portfolio:
            api.abort(404)
        else:
            return team_portfolio

    @api.response(201, 'team_portfolio successfully created.')
    @api.doc('update a team_portfolio')
    @api.expect(_team_portfolio, validate=True)
    def put(self, team_portfolio_id):
        """Update a team_portfolio """
        data = request.json
        return update_team_portfolio(team_portfolio_id, data)

    @api.response(201, 'team_portfolio successfully deleted.')
    @api.doc('delete a team_portfolio')
    def delete(self, team_portfolio_id):
        """Delete a team"""
        return delete_a_team_portfolio(team_portfolio_id)