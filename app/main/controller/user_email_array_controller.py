from flask import request
from flask_restplus import Resource, reqparse

from ..util.dto import UserEmailArrayDto
from ..service.user_team_service import save_new_user_team, get_all_user_teams, get_a_user_team, update_user_team, delete_a_user_team
from ..service.auth_helper import Auth
from ..util.decorator import token_required, admin_token_required
from ..service.user_team_service import check_user_in_team, check_user_is_owner_or_editor, check_user_is_owner
from ..service.user_service import get_a_user_by_email
import json

import datetime
api=UserEmailArrayDto.api
_user_email_array=UserEmailArrayDto.user_email_array

@api.route('/')
class UserEmailArray(Resource):
	@api.response(201, 'user_email_array successfully created.')
	@api.doc('create a new user_email_array')
	@api.expect(_user_email_array, validate=True)
	@token_required
	def post(self):
		"""Creates a new user_team"""
		data = request.json
		logined, status = Auth.get_logged_in_user(request)
		token=logined.get('data')
		if not token:
			return logined, status
		email_list=json.loads(data['data'])
		for i in email_list:
			if token['admin']==False:
				if check_user_in_team(token['user_id'], i['team_id'])==False:
					response_object = {
						'status': 'fail',
						'message': 'You cannot add this information.'
						}
					return response_object, 401
			if check_user_is_owner(token['user_id'], i['team_id'])==False:
				response_object = {
					'status': 'fail',
					'message': 'You cannot add this information.'
					}
				return response_object, 401
			login_user={"login_user_id": token['user_id']}
			action_time={"action_time": datetime.datetime.utcnow()}
			user_to_add=get_a_user_by_email(i['user_email'])
			if not user_to_add:
				response_object = {
					'status': 'fail',
					'message': 'This email is not registered.',
					'email': i['user_email']
					}
				return response_object, 404
			new_data=dict()
			new_data["team_id"]=int(i["team_id"])
			new_data["user_id"]=user_to_add.id
			new_data["role"]=i["role"]
			new_data.update(login_user)
			new_data.update(action_time)
			response_object, message = save_new_user_team(new_data)
		return response_object, message