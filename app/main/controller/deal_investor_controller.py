from flask import request
from flask_restplus import Resource

from ..util.dto import DealInvestorDto
from ..service.deal_investor_service import save_new_deal_investor, get_all_deal_investors, get_a_deal_investor, update_deal_investor, delete_a_deal_investor

api = DealInvestorDto.api
_deal_investor = DealInvestorDto.deal_investor


@api.route('/')
class DealInvestorList(Resource):
    @api.doc('list_of_deal_investor')
    @api.marshal_list_with(_deal_investor, envelope='data')
    def get(self):
        """List all deal_investors"""
        return get_all_deal_investors()

    @api.response(201, 'deal_investor successfully created.')
    @api.doc('create a new deal_investor')
    @api.expect(_deal_investor, validate=True)
    def post(self):
        """Creates a new deal_investor """
        data = request.json
        return save_new_deal_investor(data=data)

@api.route('/<deal_investor_id>')
@api.param('deal_investor_id', 'The deal investor identifier')
@api.response(404, 'deal_investor not found.')
class DealInvestor(Resource):
    @api.doc('get a deal_investor')
    @api.marshal_with(_deal_investor)
    def get(self, deal_investor_id):
        """get a deal_investor given its identifier"""
        deal_investor = get_a_deal_investor(deal_investor_id)
        if not deal_investor:
            api.abort(404)
        else:
            return deal_investor

    @api.response(201, 'deal_investor successfully created.')
    @api.doc('update a deal_investor')
    @api.expect(_deal_investor, validate=True)
    def put(self, deal_investor_id):
        """Update a deal_investor """
        data = request.json
        return update_deal_investor(deal_investor_id, data)

    @api.response(201, 'deal_investor successfully deleted.')
    @api.doc('delete a deal_investor')
    def delete(self, deal_investor_id):
        """Delete a deal_investor """
        return delete_a_deal_investor(deal_investor_id)