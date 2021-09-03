from flask import request
from flask_restplus import Resource, reqparse

from ..util.dto import PortfolioDto
from ..service.portfolio_service import save_new_portfolio, get_all_portfolios, get_a_portfolio, update_portfolio, delete_a_portfolio

api = PortfolioDto.api
_portfolio = PortfolioDto.portfolio


@api.route('/')
class PortfolioList(Resource):
    @api.doc('list_of_portfolios for a portfolio_model')
    @api.param('property_id', 'property id to search portfolios for')
    @api.param('team_id', 'team_id to search portfolios for')
    @api.marshal_list_with(_portfolio, envelope='data')
    def get(self):
        """List all portfolios"""
        parser = reqparse.RequestParser()
        parser.add_argument("property_id", type=int)
        parser.add_argument("team_id", type=int)
        args = parser.parse_args()
        return get_all_portfolios(args['property_id'], args['team_id'])

    @api.response(201, 'portfolio successfully created.')
    @api.doc('create a new portfolio')
    @api.expect(_portfolio, validate=True)
    def post(self):
        """Creates a new portfolio """
        data = request.json
        return save_new_portfolio(data=data)

@api.route('/<portfolio_id>')
@api.param('portfolio_id', 'The portfolio identifier')
@api.response(404, 'portfolio not found.')
class Portfolio(Resource):
    @api.doc('get a portfolio')
    @api.marshal_with(_portfolio)
    def get(self, portfolio_id):
        """get a portfolio given its identifier"""
        portfolio = get_a_portfolio(portfolio_id)
        if not portfolio:
            api.abort(404)
        else:
            return portfolio

    @api.response(201, 'portfolio successfully created.')
    @api.doc('update a portfolio')
    @api.expect(_portfolio, validate=True)
    def put(self, portfolio_id):
        """Update a portfolio"""
        data = request.json
        return update_portfolio(portfolio_id, data)

    @api.response(201, 'portfolio successfully deleted.')
    @api.doc('delete a portfolio')
    def delete(self, portfolio_id):
        """Delete a portfolio """
        return delete_a_portfolio(portfolio_id)