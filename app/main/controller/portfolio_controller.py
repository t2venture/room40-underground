from app.main.service.user_team_service import check_user_in_team, check_user_is_owner_or_editor, check_user_is_owner
from flask import request
from flask_restplus import Resource, reqparse
from ..util.decorator import token_required, admin_token_required
from ..util.dto import PortfolioDto
from ..service.portfolio_service import save_new_portfolio, get_all_portfolios, get_a_portfolio, update_portfolio, delete_a_portfolio
from ..service.team_portfolio_service import save_new_team_portfolio
from ..service.team_service import get_all_teams, get_a_team, get_personal_team_id, get_teams_from_portfolio, get_personal_team_id
from ..service.auth_helper import Auth
import datetime
api = PortfolioDto.api
_portfolio = PortfolioDto.portfolio


@api.route('/')
class PortfolioList(Resource):
    @api.doc('list_of_portfolios for a portfolio_model')
    @api.param('property_id', 'property id to search portfolios for')
    @api.param('team_id', 'team_id to search portfolios for')
    @api.param('is_deleted', 'if the portfolio is deleted or not')
    @api.param('is_active', 'if the portfolio is active or not')
    @api.marshal_list_with(_portfolio, envelope='data')
    @token_required
    def get(self):
        """List all portfolios"""
        parser = reqparse.RequestParser()
        parser.add_argument("property_id", type=int)
        parser.add_argument("team_id", type=int)
        parser.add_argument("is_deleted", type=bool)
        parser.add_argument("is_active", type=bool)
        args = parser.parse_args()
        logined, status = Auth.get_logged_in_user(request)
        token=logined.get('data')
        if not token:
            return logined, status
        if token["admin"]==False:
            args["team_id"]=get_personal_team_id(token["user_id"])['id']
        #non admins will see the portfolios they have created if they search for portfolios without specifying team id
        return get_all_portfolios(args['property_id'], args['team_id'], args["is_deleted"], args["is_active"])

    @api.response(201, 'portfolio successfully created.')
    @api.doc('create a new portfolio')
    @api.expect(_portfolio, validate=True)
    @token_required
    def post(self):
        """Creates a new portfolio """
        data = request.json
        logined, status = Auth.get_logged_in_user(request)
        token=logined.get('data')
        if not token:
            return logined, status
        login_user={"login_user_id": token['user_id']}
        action_time={"action_time": datetime.datetime.utcnow()}
        data.update(login_user)
        data.update(action_time)
        personal_team=get_personal_team_id(login_user)
        personal_team_id={"personal_team_id": personal_team["id"]}
        data.update(personal_team_id)
        return save_new_portfolio(data=data)
        #This also creates the entry in TeamPortfolio as to which team member is the owner of the portfolio.

@api.route('/<portfolio_id>')
@api.param('portfolio_id', 'The portfolio identifier')
@api.response(404, 'portfolio not found.')
class Portfolio(Resource):
    @api.doc('get a portfolio')
    @api.marshal_with(_portfolio)
    @token_required
    def get(self, portfolio_id):
        """get a portfolio given its identifier"""
        portfolio = get_a_portfolio(portfolio_id)
        logined, status = Auth.get_logged_in_user(request)
        token=logined.get('data')
        if not token:
            return logined, status
        usr_id=token['user_id']
        allowed_teams=get_teams_from_portfolio(portfolio_id)
        #Checking is User can VIEW the portfolio
        flag=False
        for team in allowed_teams:
            team_id=team["id"]
            if check_user_in_team(usr_id, team_id)==True:
                flag=True
        if flag==False and token['admin']==False:
            response_object = {
                'status': 'fail',
                'message': 'You cannot search for this information.'
                }
            return response_object, 401
        if not portfolio:
            api.abort(404)
        else:
            return portfolio

    @api.response(201, 'portfolio successfully created.')
    @api.doc('update a portfolio')
    @api.expect(_portfolio, validate=True)
    @token_required
    def put(self, portfolio_id):
        """Update a portfolio"""
        data = request.json
        logined, status = Auth.get_logged_in_user(request)
        token=logined.get('data')
        if not token:
            return logined, status
        login_user={"login_user_id": token['user_id']}
        action_time={"action_time": datetime.datetime.utcnow()}
        allowed_teams=get_teams_from_portfolio(portfolio_id)
        flag=False
        for team in allowed_teams:
            if team["role"]=="Owner" or team["role"]=="Editor":
                if check_user_is_owner_or_editor(token['user_id'],team["team_id"])==True:
                    flag=True
        if flag==False and token['admin']==False:
            response_object = {
                'status': 'fail',
                'message': 'You cannot add this information.'
                }
            return response_object, 401
        data.update(login_user)
        data.update(action_time)
        return update_portfolio(portfolio_id, data)

    @api.response(201, 'portfolio successfully deleted.')
    @api.doc('delete a portfolio')
    @token_required
    def delete(self, portfolio_id, data):
        """Delete a portfolio """
        logined, status = Auth.get_logged_in_user(request)
        token=logined.get('data')
        if not token:
            return logined, status
        login_user={"login_user_id": token['user_id']}
        action_time={"action_time": datetime.datetime.utcnow()}
        allowed_teams=get_teams_from_portfolio(portfolio_id)
        flag=False
        for team in allowed_teams:
            if team["role"]=="Owner" or team["role"]=="Editor":
                if check_user_is_owner_or_editor(token['user_id'],team["team_id"])==True:
                    flag=True
        if flag==False and token['admin']==False:
            response_object = {
                'status': 'fail',
                'message': 'You cannot delete this information.'
                }
            return response_object, 401
        data=dict()
        data.update(login_user)
        data.update(action_time)
        return delete_a_portfolio(portfolio_id, data)