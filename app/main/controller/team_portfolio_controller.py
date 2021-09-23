from flask import request
from flask_restplus import Resource,reqparse
from ..util.decorator import token_required, admin_token_required

from ..util.dto import TeamPortfolioDto
from ..service.team_portfolio_service import save_new_team_portfolio, get_all_team_portfolios, get_a_team_portfolio, update_team_portfolio, delete_a_team_portfolio
from ..service.auth_helper import Auth
import datetime

api = TeamPortfolioDto.api
_team_portfolio = TeamPortfolioDto.team_portfolio


@api.route('/')
class TeamPortfolioList(Resource):
    @api.doc('list_of_team_portfolios for a team_portfolio')
    @api.param('is_deleted', 'whether the property model is deleted or not')
    @api.param('is_active', 'whether the property model is active or not')
    @api.marshal_list_with(_team_portfolio, envelope='data')
    def get(self):
        """List all team_portfolios"""
        parser = reqparse.RequestParser()
        parser.add_argument("is_deleted", type=bool)
        parser.add_argument("is_active", type=bool)
        args=parser.parse_args()
        return get_all_team_portfolios(args["is_deleted"], args["is_active"])

    @api.response(201, 'team_portfolio successfully created.')
    @api.doc('create a new team_portfolio')
    @api.expect(_team_portfolio, validate=True)
    def post(self):
        """Creates a new team_portfolio """
        data = request.json
        logined, status = Auth.get_logged_in_user(request)
        token=logined.get('data')
        if not token:
            return logined, status
        login_user={"login_user_id": token['user_id']}
        action_time={"action_time": datetime.datetime.utcnow()}
        data.update(login_user)
        data.update(action_time)
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
        logined, status = Auth.get_logged_in_user(request)
        token=logined.get('data')
        if not token:
            return logined, status
        login_user={"login_user_id": token['user_id']}
        action_time={"action_time": datetime.datetime.utcnow()}
        data.update(login_user)
        data.update(action_time)
        return update_team_portfolio(team_portfolio_id, data)

    @api.response(201, 'team_portfolio successfully deleted.')
    @api.doc('delete a team_portfolio')
    def delete(self, team_portfolio_id, data):
        """Delete a team"""
        logined, status = Auth.get_logged_in_user(request)
        token=logined.get('data')
        if not token:
            return logined, status
        data=dict()
        login_user={"login_user_id": token['user_id']}
        action_time={"action_time": datetime.datetime.utcnow()}
        data.update(login_user)
        data.update(action_time)	
        return delete_a_team_portfolio(team_portfolio_id)