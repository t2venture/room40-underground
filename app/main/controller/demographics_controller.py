from flask import request
from flask_restplus import Resource, reqparse

from ..util.dto import DemographicsDto

import json
import datetime
from ..util.decorator import token_required, admin_token_required
from ..util.get_demographics import summarize_stats
api = DemographicsDto.api
_demographics = DemographicsDto.demographics

@api.route('/')
class Demographics(Resource):
	@api.doc('demographics for a particular geography id')
	@api.marshal_list_with(_demographics, envelope='data')
	@api.param("geography_id", "geography_id of the region you want demographics for")
	@token_required
	def get(self):
	    '''List all documents'''
	    parser = reqparse.RequestParser()
	    parser.add_argument("geography_id", type=str)
	    args = parser.parse_args()
	    return summarize_stats(args["geography_id"])
