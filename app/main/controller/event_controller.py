from flask import request
from flask_restplus import Resource, reqparse

from ..util.dto import EventDto
from ..service.event_service import save_new_event, get_all_events, get_a_event, update_event, delete_a_event

api = EventDto.api
_event = EventDto.event


@api.route('/')
class EventList(Resource):
    @api.doc('list_of_events for a event')
    @api.param('deal_id', 'The deal identifier')
    @api.param('week', 'Get events for the current week')
    @api.marshal_list_with(_event, envelope='data')
    def get(self):
        """List all events"""
        parser = reqparse.RequestParser()
        parser.add_argument("deal_id", type=int)
        parser.add_argument("week", type=bool)
        args = parser.parse_args()
        return get_all_events(args['deal_id'], args['week'])

    @api.response(201, 'event successfully created.')
    @api.doc('create a new event')
    @api.expect(_event, validate=True)
    def post(self):
        """Creates a new event """
        data = request.json
        return save_new_event(data=data)

@api.route('/<event_id>')
@api.param('event_id', 'The event identifier')
@api.response(404, 'Event not found.')
class Event(Resource):
    @api.doc('get a event')
    @api.marshal_with(_event)
    def get(self, event_id):
        """get a event given its identifier"""
        event = get_a_event(event_id)
        if not event:
            api.abort(404)
        else:
            return event

    @api.response(201, 'event successfully created.')
    @api.doc('update a event')
    @api.expect(_event, validate=True)
    def put(self, event_id):
        """Update a event """
        data = request.json
        return update_event(event_id, data)

    @api.response(201, 'event successfully deleted.')
    @api.doc('delete a event')
    def delete(self, event_id):
        """Delete a event """
        return delete_a_event(event_id)