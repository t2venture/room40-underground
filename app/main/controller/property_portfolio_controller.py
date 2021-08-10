from flask import request
from flask_restplus import Resource

from ..util.dto import PropertyPortfolioDto
from ..service.property_portfolio_service import save_new_property_portfolio, get_all_property_portfolios, get_a_property_portfolio, update_property_portfolio, delete_a_property_portfolio

api = PropertyPortfolioDto.api
_property_portfolio = PropertyPortfolioDto.property_portfolio


@api.route('/')
class PropertyPortfolioList(Resource):
    @api.doc('list_of_property_portfolios for a property_portfolio')
    @api.marshal_list_with(_property_portfolio, envelope='data')
    def get(self):
        """List all property_portfolios"""
        return get_all_property_portfolios()

    @api.response(201, 'property_portfolio successfully created.')
    @api.doc('create a new property_portfolio')
    @api.expect(_property_portfolio, validate=True)
    def post(self):
        """Creates a new property_portfolio """
        data = request.json
        return save_new_property_portfolio(data=data)

@api.route('/<property_portfolio_id>')
@api.param('property_portfolio_id', 'The property_portfolio identifier')
@api.response(404, 'property_portfolio not found.')
class PropertyPortfolio(Resource):
    @api.doc('get a property_portfolio')
    @api.marshal_with(_property_portfolio)
    def get(self, property_portfolio_id):
        """get a property_portfolio given its identifier"""
        property_portfolio = get_a_property_portfolio(property_portfolio_id)
        if not property_portfolio:
            api.abort(404)
        else:
            return property_portfolio

    @api.response(201, 'property_portfolio successfully created.')
    @api.doc('update a property_portfolio')
    @api.expect(_property_portfolio, validate=True)
    def put(self, property_portfolio_id):
        """Update a property_portfolio """
        data = request.json
        return update_property_portfolio(property_portfolio_id, data)

    @api.response(201, 'property_portfolio successfully deleted.')
    @api.doc('delete a property_portfolio')
    def delete(self, property_portfolio_id):
        """Delete a property"""
        return delete_a_property_portfolio(property_portfolio_id)