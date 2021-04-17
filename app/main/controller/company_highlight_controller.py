from flask import request
from flask_restplus import Resource

from ..util.dto import CompanyHighlightDto
from ..service.company_highlight_service import save_new_company_highlight, get_all_company_highlights, get_a_company_highlight

api = CompanyHighlightDto.api
_company_highlight = CompanyHighlightDto.company_highlight


@api.route('/')
class CompanyHighlightList(Resource):
    @api.doc('list_of_company_highlight')
    @api.marshal_list_with(_company_highlight, envelope='data')
    def get(self):
        """List all company_highlights"""
        return get_all_company_highlights()

    @api.response(201, 'company_highlight successfully created.')
    @api.doc('create a new company_highlight')
    @api.expect(_company_highlight, validate=True)
    def post(self):
        """Creates a new company_highlight"""
        data = request.json
        return save_new_company_highlight(data=data)

@api.route('/<company_highlight_id>')
@api.param('company_highlight_id', 'The company highlight identifier')
@api.response(404, 'company_highlight not found.')
class CompanyHighlight(Resource):
    @api.doc('get a company_highlight')
    @api.marshal_with(_company_highlight)
    def get(self, company_highlight_id):
        """get a company_highlight given its identifier"""
        company_highlight = get_a_company_highlight(company_highlight_id)
        if not company_highlight:
            api.abort(404)
        else:
            return company_highlight