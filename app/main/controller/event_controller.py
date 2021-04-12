from flask import request
from flask_restplus import Resource

from ..util.dto import EventDto
from ..service.event_service import save_new_event, get_all_events, get_a_event

api = EventDto.api
_event = EventDto.event


@api.route('/')
@api.param('deal_id', 'The deal identifier')
class EventList(Resource):
    @api.doc('list_of_events for a event')
    @api.marshal_list_with(_event, envelope='data')
    def get(self, deal_id):
        """List all events"""
        return get_all_events(deal_id)

    @api.response(201, 'event successfully created.')
    @api.doc('create a new event')
    @api.expect(_event, validate=True)
    def post(self, deal_id):
        """Creates a new event """
        data = request.json
        return save_new_event(deal_id, data=data)

@api.route('/<event_id>')
@api.param('deal_id', 'The deal identifier')
@api.param('event_id', 'The event identifier')
@api.response(404, 'Event not found.')
class Event(Resource):
    @api.doc('get a event')
    @api.marshal_with(_event)
    def get(self, deal_id, event_id):
        """get a event given its identifier"""
        event = get_a_event(event_id)
        if not event:
            api.abort(404)
        else:
            return event