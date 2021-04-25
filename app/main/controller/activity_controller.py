from flask import request
from flask_restplus import Resource, reqparse

from ..util.dto import ActivityDto
from ..service.activity_service import save_new_activity, get_all_activities, get_a_activity, update_activity, delete_a_activity

api = ActivityDto.api
_activity = ActivityDto.activity


@api.route('/')
class ActivityList(Resource):
    @api.doc('list_of_activities for a company')
    @api.param('company_id', 'The company identifier')
    @api.param('due_date', 'Find all activities before this date')
    @api.param('priority', 'Search by priority')
    @api.param('title', 'title of activity')
    @api.marshal_list_with(_activity, envelope='data')
    def get(self):
        """List all registered users"""
        parser = reqparse.RequestParser()
        parser.add_argument("company_id", type=int)
        parser.add_argument("due_date", type=str)
        parser.add_argument("priority", type=str)
        parser.add_argument("title", type=str)
        args = parser.parse_args()
        return get_all_activities(args['company_id'], args["due_date"], args["priority"], args["title"])

    @api.response(201, 'Activity successfully created.')
    @api.doc('create a new activity')
    @api.expect(_activity, validate=True)
    def post(self):
        """Creates a new Activity"""
        data = request.json
        return save_new_activity(data=data)

@api.route('/<activity_id>')
@api.param('activity_id', 'The Activity identifier')
@api.response(404, 'Activity not found.')
class Activity(Resource):
    @api.doc('get a activty')
    @api.marshal_with(_activity)
    def get(self, activity_id):
        """get a user given its identifier"""
        activity = get_a_activity(activity_id)
        if not activity:
            api.abort(404)
        else:
            return activity

    @api.response(201, 'activity successfully created.')
    @api.doc('update a activity')
    @api.expect(_activity, validate=True)
    def put(self, activity_id):
        """Update a activity """
        data = request.json
        return update_activity(activity_id, data)

    @api.response(201, 'activity successfully deleted.')
    @api.doc('delete a activity')
    def delete(self, activity_id):
        """Delete a activity """
        return delete_a_activity(activity_id)