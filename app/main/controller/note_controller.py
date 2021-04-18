from flask import request
from flask_restplus import Resource, reqparse

from ..util.dto import NoteDto
from ..service.note_service import save_new_note, get_all_notes, get_a_note

api = NoteDto.api
_note = NoteDto.note


@api.route('/')
class NoteList(Resource):
    @api.doc('list_of_notes for a note')
    @api.param('deal_id', 'deal this note is associated with')
    @api.param('search_query', 'search through keywords, categories, and body')
    @api.marshal_list_with(_note, envelope='data')
    def get(self):
        """List all notes"""
        parser = reqparse.RequestParser()
        parser.add_argument("deal_id", type=int)
        parser.add_argument("search_query", type=str)
        args = parser.parse_args()
        return get_all_notes(args['deal_id'], args['search_query'])

    @api.response(201, 'note successfully created.')
    @api.doc('create a new note')
    @api.expect(_note, validate=True)
    def post(self, deal_id):
        """Creates a new note """
        data = request.json
        return save_new_note(data=data)

@api.route('/<note_id>')
@api.param('note_id', 'The note identifier')
@api.response(404, 'Note not found.')
class Note(Resource):
    @api.doc('get a note')
    @api.marshal_with(_note)
    def get(self, note_id):
        """get a note given its identifier"""
        note = get_a_note(note_id)
        if not note:
            api.abort(404)
        else:
            return note