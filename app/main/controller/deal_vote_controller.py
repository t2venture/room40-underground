from flask import request
from flask_restplus import Resource

from ..util.dto import DealVoteDto
from ..service.deal_vote_service import save_new_deal_vote, get_all_deal_votes, get_a_deal_vote

api = DealVoteDto.api
_deal_vote = DealVoteDto.deal_vote


@api.route('/')
class DealVoteList(Resource):
    @api.doc('list_of_deal_vote')
    @api.marshal_list_with(_deal_vote, envelope='data')
    def get(self):
        """List all deal_votes"""
        return get_all_deal_votes()

    @api.response(201, 'deal_vote successfully created.')
    @api.doc('create a new deal_vote')
    @api.expect(_deal_vote, validate=True)
    def post(self):
        """Creates a new deal_vote """
        data = request.json
        return save_new_deal_vote(data=data)

@api.route('/<deal_vote_id>')
@api.param('deal_vote_id', 'The deal vote identifier')
@api.response(404, 'deal_vote not found.')
class DealVote(Resource):
    @api.doc('get a deal_vote')
    @api.marshal_with(_deal_vote)
    def get(self, deal_vote_id):
        """get a deal_vote given its identifier"""
        deal_vote = get_a_deal_vote(deal_vote_id)
        if not deal_vote:
            api.abort(404)
        else:
            return deal_vote