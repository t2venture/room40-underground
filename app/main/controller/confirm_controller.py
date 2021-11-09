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
    @api.response(201, 'token confirmed!')
    @api.param('token', 'your confirmation token')
    @api.param('new_password', 'setting your password')
    def post(self):
        '''Verifies the token sent'''
        parser = reqparse.RequestParser()
        parser.add_argument("token", type=str)
        parser.add_argument("new_password", type=str)
        args = parser.parse_args()
        if args['new_password']:
            return verify_reset_email(args['token'], args["new_password"])
        else:
            return confirm_email(args['token'])

