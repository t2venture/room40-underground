from flask import request
from flask_restplus import Resource, reqparse
import datetime
import json
from ..util.decorator import token_required, admin_token_required
from ..util.dto import PersonalTeamDto
from ..service.team_service import get_personal_team_id
api=PersonalTeamDto.api
_personal_team=PersonalTeamDto.personal_team

@api.route('/')
class PersonalTeam(Resource):
	@api.doc('get personal team id')
	@api.param('user_id', 'user_id to search personal team for')
	@token_required
	def get(self):
		parser = reqparse.RequestParser()
		parser.add_argument("user_id", type=int)
		args=parser.parse_args()
		if not args['user_id']:
			return_obj={"status": "fail", "message": "You need to input an user id"}
			return return_obj, 400
		user_id_to_search=int(args['user_id'])
		team_to_return=get_personal_team_id(user_id_to_search)
		if not team_to_return:
			return_obj={"status": "fail", "message": "User doesn't exist"}
			return return_obj, 404
		personal_id=team_to_return.id
		personal_team_obj={
			"personal_team_id": personal_id,
			"status": "success",
			"message": "You succesfully queried the personal team ID."
			}
		return personal_team_obj, 200
