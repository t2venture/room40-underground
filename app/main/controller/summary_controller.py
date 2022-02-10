from flask import request
from flask_restplus import Resource, reqparse

from ..util.dto import SummaryDto
from ..service.summary_service import save_new_summary, get_a_summary, get_all_summaries, delete_a_summary
from ..service.auth_helper import Auth
import datetime
api = SummaryDto.api
_summary = SummaryDto.summary

@api.route('/')
class Summary(Resource):
	@api.doc('summary resource given a zipcode parameter')
	@api.param('zipcode', 'zipcode to search for')
	@api.summary(_summary, validate=True)
	def get(self):
		parser=reqparse.RequestParser()
		parser.add_argument('zipcode', type=int)
		args=parser.parse_args()
		logined, status = Auth.get_logged_in_user(request)
		token=logined.get('data')
		token["user_id"]=int(token["user_id"])
		summary_to_output=get_all_summaries(args['zipcode'])
		return summary_to_output
