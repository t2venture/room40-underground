from flask import request
from flask_restplus import Resource, reqparse

from ..util.dto import HighlightDto
from ..service.highlight_service import save_new_highlight, get_all_highlights, get_a_highlight

api = HighlightDto.api
_highlight = HighlightDto.highlight


@api.route('/')
class NoteList(Resource):
    @api.doc('list_of_highlights for a highlight')
    @api.param('company_id', 'company that the highlights are associated with')
    @api.marshal_list_with(_highlight, envelope='data')
    def get(self):
        """List all highlights"""
        parser = reqparse.RequestParser()
        parser.add_argument("company_id", type=int)
        args = parser.parse_args()
        return get_all_highlights(args["company_id"])

    @api.response(201, 'highlight successfully created.')
    @api.doc('create a new highlight')
    @api.expect(_highlight, validate=True)
    def post(self):
        """Creates a new highlight """
        data = request.json
        return save_new_highlight(data=data)

@api.route('/<highlight_id>')
@api.param('highlight_id', 'The highlight identifier')
@api.response(404, 'Note not found.')
class Note(Resource):
    @api.doc('get a highlight')
    @api.marshal_with(_highlight)
    def get(self, highlight_id):
        """get a highlight given its identifier"""
        highlight = get_a_highlight(highlight_id)
        if not highlight:
            api.abort(404)
        else:
            return highlight