from flask import request
from flask_restplus import Resource, reqparse
import datetime

from app.main.service.user_service import get_a_user, update_password_user, update_user
from ..util.dto import ChangepasswordDto
import json
from ..service.auth_helper import Auth
from ..util.decorator import token_required, admin_token_required
api=ChangepasswordDto.api
changepassword=ChangepasswordDto.changepassword

@api.route('/')

class Changepassword(Resource):
	@api.doc('change password')
	@api.response('201', 'password changed, login again')
	@api.param('oldpassword', 'old password')
	@api.param('newpassword', 'new password')
	@token_required
	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument("oldpassword", type=str)
		parser.add_argument("newpassword", type=str)
		args = parser.parse_args()
		logined, status = Auth.get_logged_in_user(request)
		token=logined.get('data')
		usr_id=int(token['user_id'])
		user_to_change=get_a_user(usr_id)
		flag=user_to_change.check_password(args['oldpassword'])
		if flag==False:
			response_object = {
				'status': 'fail',
				'message': 'email or password does not match.'
				}
			return response_object, 401

		elif not args['newpassword']:
			response_object = {
				'status': 'fail',
				'message': 'The new password must be non empty.'
				}
			return response_object, 401
		else:
			data={"password": args['newpassword']}
			return update_user(usr_id, data)