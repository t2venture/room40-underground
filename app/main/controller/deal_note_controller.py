from flask import request
from flask_restplus import Resource

from ..util.dto import DealNoteDto
from ..service.deal_note_service import save_new_deal_note, get_all_deal_notes, get_a_deal_note

api = DealNoteDto.api
_deal_note = DealNoteDto.deal_note


@api.route('/')
class DealNoteList(Resource):
    @api.doc('list_of_deal_note')
    @api.marshal_list_with(_deal_note, envelope='data')
    def get(self):
        """List all deal_notes"""
        return get_all_deal_notes()

    @api.response(201, 'deal_note successfully created.')
    @api.doc('create a new deal_note')
    @api.expect(_deal_note, validate=True)
    def post(self):
        """Creates a new deal_note """
        data = request.json
        return save_new_deal_note(data=data)

@api.route('/<deal_note_id>')
@api.param('deal_note_id', 'The deal note identifier')
@api.response(404, 'deal_note not found.')
class DealNote(Resource):
    @api.doc('get a deal_note')
    @api.marshal_with(_deal_note)
    def get(self, deal_note_id):
        """get a deal_note given its identifier"""
        deal_note = get_a_deal_note(deal_note_id)
        if not deal_note:
            api.abort(404)
        else:
            return deal_note