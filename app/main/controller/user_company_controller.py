from flask import request
from flask_restplus import Resource

from ..util.dto import UserCompanyDto
from ..service.user_company_service import save_new_user_company, get_all_user_companies, get_a_user_company

api = UserCompanyDto.api
_user_company = UserCompanyDto.user_company


@api.route('/')
class UserCompanyList(Resource):
    @api.doc('list_of_user_companies')
    @api.marshal_list_with(_user_company, envelope='data')
    def get(self):
        """List all user_companies"""
        return get_all_user_companies()

    @api.response(201, 'user_company successfully created.')
    @api.doc('create a new user_company')
    @api.expect(_user_company, validate=True)
    def post(self):
        """Creates a new user_company """
        data = request.json
        return save_new_user_company(data=data)

@api.route('/<user_company_id>')
@api.param('user_company_id', 'The event participant identifier')
@api.response(404, 'user_company not found.')
class UserCompany(Resource):
    @api.doc('get a user_company')
    @api.marshal_with(_user_company)
    def get(self, user_company_id):
        """get a user_company given its identifier"""
        user_company = get_a_user_company(user_company_id)
        if not user_company:
            api.abort(404)
        else:
            return user_company