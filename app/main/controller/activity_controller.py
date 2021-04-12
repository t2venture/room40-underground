from flask import request
from flask_restplus import Resource

from ..util.dto import ActivityDto
from ..service.activity_service import save_new_activity, get_all_activities, get_a_activity

api = ActivityDto.api
_activity = ActivityDto.activity


@api.route('/')
class ActivityList(Resource):
    @api.doc('list_of_activities for a company')
    @api.marshal_list_with(_activity, envelope='data')
    def get(self, company_id):
        """List all registered users"""
        return get_all_activities(company_id)

    @api.response(201, 'Activity successfully created.')
    @api.doc('create a new activity')
    @api.expect(_activity, validate=True)
    def post(self, company_id):
        """Creates a new Activity """
        data = request.json
        return save_new_activity(company_id, data=data)

@api.route('/<activity_id>')
@api.param('company_id', 'The Company identifier')
@api.param('activity_id', 'The Activity identifier')
@api.response(404, 'Activity not found.')
class Activity(Resource):
    @api.doc('get a activty')
    @api.marshal_with(_activity)
    def get(self, company_id, activity_id):
        """get a user given its identifier"""
        activity = get_a_activity(company_id, activity_id)
        if not activity:
            api.abort(404)
        else:
            return activity