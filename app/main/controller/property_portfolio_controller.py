from flask import request
from flask_restplus import Resource, reqparse
from ..util.decorator import token_required, admin_token_required
from ..util.dto import PropertyPortfolioDto
from ..service.property_portfolio_service import save_new_property_portfolio, get_all_property_portfolios, get_a_property_portfolio, update_property_portfolio, delete_a_property_portfolio
from ..service.auth_helper import Auth
import datetime
api = PropertyPortfolioDto.api
_property_portfolio = PropertyPortfolioDto.property_portfolio


@api.route('/')
class PropertyPortfolioList(Resource):
    @api.doc('list_of_property_portfolios for a property_portfolio')
    @api.param('is_deleted', 'whether the property model is deleted or not')
    @api.param('is_active', 'whether the property model is active or not')
    @api.marshal_list_with(_property_portfolio, envelope='data')
    @token_required
    def get(self):
        """List all property_portfolios"""
        parser = reqparse.RequestParser()
        parser.add_argument("is_deleted", type=bool)
        parser.add_argument("is_active", type=bool)
        args = parser.parse_args()
        return get_all_property_portfolios(args["is_deleted"], args["is_active"])

    @api.response(201, 'property_portfolio successfully created.')
    @api.doc('create a new property_portfolio')
    @api.expect(_property_portfolio, validate=True)
    @token_required
    def post(self):
        """Creates a new property_portfolio """
        data = request.json
        logined, status = Auth.get_logged_in_user(request)
        token=logined.get('data')
        if not token:
            return logined, status
        login_user={"login_user_id": token['user_id']}
        action_time={"action_time": datetime.datetime.utcnow()}
        data.update(login_user)
        data.update(action_time)
        return save_new_property_portfolio(data=data)

@api.route('/<property_portfolio_id>')
@api.param('property_portfolio_id', 'The property_portfolio identifier')
@api.response(404, 'property_portfolio not found.')
class PropertyPortfolio(Resource):
    @api.doc('get a property_portfolio')
    @api.marshal_with(_property_portfolio)
    @token_required
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
    @token_required
    def put(self, property_portfolio_id):
        """Update a property_portfolio """
        data = request.json
        return update_property_portfolio(property_portfolio_id, data)

    @api.response(201, 'property_portfolio successfully deleted.')
    @api.doc('delete a property_portfolio')
    @token_required
    def delete(self, property_portfolio_id):
        """Delete a property"""
        return delete_a_property_portfolio(property_portfolio_id, data)