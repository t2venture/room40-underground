from flask import request
from flask_restplus import Resource

from ..util.dto import EventParticipantDto
from ..service.event_participant_service import save_new_event_participant, get_all_event_participants, get_a_event_participant

api = EventParticipantDto.api
_event_participant = EventParticipantDto.event_participant


@api.route('/')
class EventParticipantList(Resource):
    @api.doc('list_of_event_participants')
    @api.marshal_list_with(_event_participant, envelope='data')
    def get(self):
        """List all event_participants"""
        return get_all_event_participants()

    @api.response(201, 'event_participant successfully created.')
    @api.doc('create a new event_participant')
    @api.expect(_event_participant, validate=True)
    def post(self):
        """Creates a new event_participant """
        data = request.json
        return save_new_event_participant(data=data)

@api.route('/<event_participant_id>')
@api.param('event_participant_id', 'The event participant identifier')
@api.response(404, 'event_participant not found.')
class EventParticipant(Resource):
    @api.doc('get a event_participant')
    @api.marshal_with(_event_participant)
    def get(self, event_participant_id):
        """get a event_participant given its identifier"""
        ep = get_a_event_participant(event_participant_id)
        if not ep:
            api.abort(404)
        else:
            return ep