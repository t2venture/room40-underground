from flask import request
from flask_restplus import Resource

from ..util.dto import HighlightDto
from ..service.highlight_service import save_new_highlight, get_all_highlights, get_a_highlight

api = HighlightDto.api
_highlight = HighlightDto.highlight


@api.route('/')
@api.param('company_id', 'The company identifier')
class NoteList(Resource):
    @api.doc('list_of_highlights for a highlight')
    @api.marshal_list_with(_highlight, envelope='data')
    def get(self, company_id):
        """List all highlights"""
        return get_all_highlights(company_id)

    @api.response(201, 'highlight successfully created.')
    @api.doc('create a new highlight')
    @api.expect(_highlight, validate=True)
    def post(self, company_id):
        """Creates a new highlight """
        data = request.json
        return save_new_highlight(company_id, data=data)

@api.route('/<highlight_id>')
@api.param('company_id', 'The company identifier')
@api.param('highlight_id', 'The highlight identifier')
@api.response(404, 'Note not found.')
class Note(Resource):
    @api.doc('get a highlight')
    @api.marshal_with(_highlight)
    def get(self, company_id, highlight_id):
        """get a highlight given its identifier"""
        highlight = get_a_highlight(highlight_id)
        if not highlight:
            api.abort(404)
        else:
            return highlight