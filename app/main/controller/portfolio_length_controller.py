from flask import request
from flask_restplus import Resource, reqparse
from flask_restplus.fields import String
from ..util.decorator import token_required, admin_token_required
from ..util.dto import PortfolioLengthDto
from ..service.team_service import get_teams_from_portfolio
from ..service.auth_helper import Auth
from ..service.user_team_service import check_user_in_team
from ..service.property_service import get_all_propertys
import datetime

api=PortfolioLengthDto.dto 
_portfolio_length=PortfolioLengthDto.portfolio_length

@api.route('/')
class PortfolioLength(Resource):
	@api.doc('get portfolio length')
	@api.param('portfolio_id', 'portfolio_id to search length for')
	@token_required
	def get(self):
		parser = reqparse.RequestParser()
		parser.add_argument("portfolio_id", type=int)
		args=parser.parse_args()
		if not args['portfolio_id']:
			return_obj={"status": "fail", "message": "You need to input a portfolio id"}
			return return_obj, 400
		p_id=int(args['portfolio_id'])
		logined, status = Auth.get_logged_in_user(request)
		token=logined.get('data')
		if not token:
			return logined, status
		usr_id=int(token['user_id'])
		allowed_teams=get_teams_from_portfolio(p_id)
		flag=False
		for team in allowed_teams:
			team_id=int(team.id)
			if check_user_in_team(usr_id, team_id)==True:
				flag=True
		if flag==False and token['admin']==False:
			response_object = {
				'status': 'fail',
				'message': 'You cannot search for this information.'
				}
			return response_object, 401
		propertys=list(get_all_propertys(portfolio_id=p_id))
		response_object = {
			"status": "success",
			"message": "You succesfully obtained the portfolio length",
			"length": len(propertys)
			}
		return response_object, 200


