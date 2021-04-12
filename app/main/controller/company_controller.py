from flask import request
from flask_restplus import Resource

from ..util.dto import CompanyDto
from ..service.company_service import save_new_company, get_all_companies, get_a_company

api = CompanyDto.api
_company = CompanyDto.company


@api.route('/')
class CompanyList(Resource):
    @api.doc('list_of_companies for a company')
    @api.marshal_list_with(_company, envelope='data')
    def get(self):
        """List all companies"""
        return get_all_companies()

    @api.response(201, 'Company successfully created.')
    @api.doc('create a new company')
    @api.expect(_company, validate=True)
    def post(self):
        """Creates a new Company """
        data = request.json
        return save_new_company(data=data)

@api.route('/<company_id>')
@api.param('company_id', 'The Company identifier')
@api.response(404, 'Company not found.')
class Company(Resource):
    @api.doc('get a company')
    @api.marshal_with(_company)
    def get(self, company_id):
        """get a company given its identifier"""
        company = get_a_company(company_id)
        if not company:
            api.abort(404)
        else:
            return company