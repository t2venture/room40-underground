from flask import request
from flask_restplus import Resource, reqparse
import datetime
from app.main.service.user_service import confirm_email, verify_reset_email
from ..util.dto import ConfirmDto
import json
api = ConfirmDto.api
user_confirm=ConfirmDto.user_confirm

@api.route('/')
class TokenConfirmation(Resource):
	@api.doc('confirm a token')
	@api.response(201,'token confirmed!')
	def post(self):
		'''Verifies the token sent'''
		data=request.json
		token=data["token"]
		if 'password' in data.keys():
			verify_reset_email(token, data["password"])
		else:
			confirm_email(token)

