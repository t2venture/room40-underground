from flask import request
from flask_restplus import Resource

from ..util.dto import DealDto
from ..service.deal_service import save_new_deal, get_all_deals, get_a_deal

api = DealDto.api
_deal = DealDto.deal


@api.route('/')
class DealList(Resource):
    @api.doc('list_of_deals for a deal')
    @api.marshal_list_with(_deal, envelope='data')
    def get(self):
        """List all deals"""
        return get_all_deals()

    @api.response(201, 'deal successfully created.')
    @api.doc('create a new deal')
    @api.expect(_deal, validate=True)
    def post(self):
        """Creates a new deal """
        data = request.json
        return save_new_deal(data=data)

@api.route('/<deal_id>')
@api.param('deal_id', 'The deal identifier')
@api.response(404, 'Deal not found.')
class Deal(Resource):
    @api.doc('get a deal')
    @api.marshal_with(_deal)
    def get(self, deal_id):
        """get a deal given its identifier"""
        deal = get_a_deal(deal_id)
        if not deal:
            api.abort(404)
        else:
            return deal