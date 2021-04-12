from flask import request
from flask_restplus import Resource

from ..util.dto import NoteDto
from ..service.note_service import save_new_note, get_all_notes, get_a_note

api = NoteDto.api
_note = NoteDto.note


@api.route('/')
@api.param('deal_id', 'The deal identifier')
class NoteList(Resource):
    @api.doc('list_of_notes for a note')
    @api.marshal_list_with(_note, envelope='data')
    def get(self, deal_id):
        """List all notes"""
        return get_all_notes(deal_id)

    @api.response(201, 'note successfully created.')
    @api.doc('create a new note')
    @api.expect(_note, validate=True)
    def post(self, deal_id):
        """Creates a new note """
        data = request.json
        return save_new_note(deal_id, data=data)

@api.route('/<note_id>')
@api.param('deal_id', 'The deal identifier')
@api.param('note_id', 'The note identifier')
@api.response(404, 'Note not found.')
class Note(Resource):
    @api.doc('get a note')
    @api.marshal_with(_note)
    def get(self, deal_id, note_id):
        """get a note given its identifier"""
        note = get_a_note(note_id)
        if not note:
            api.abort(404)
        else:
            return note