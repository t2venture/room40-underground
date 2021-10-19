from flask import request
from flask_restplus import Resource, reqparse
import datetime
from app.main.service.user_service import confirm_email
from ..util.dto import ConfirmDto

api = ConfirmDto.api
user_confirm=ConfirmDto.user_confirm





@api.route('<token>')
@api.param('token', 'the confirmation token')
class Token(Resource):
	@api.doc('confirm a token')
	@api.response(201,'token confirmed!')
	@api.expect(user_confirm, validate=True)
	def post(self, token):
		confirm_email(token)

