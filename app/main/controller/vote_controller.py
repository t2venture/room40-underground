from flask import request
from flask_restplus import Resource, reqparse

from ..util.dto import VoteDto
from ..service.vote_service import save_new_vote, get_all_votes, get_a_vote

api = VoteDto.api
_vote = VoteDto.vote


@api.route('/')
class VoteList(Resource):

    @api.doc('list_of_votes for a vote')
    @api.param('deal_id', "the deal id passed in")
    @api.marshal_list_with(_vote, envelope='data')
    def get(self):
        """List all votes"""
        parser = reqparse.RequestParser()
        parser.add_argument("deal_id", type=int)
        args = parser.parse_args()
        return get_all_votes(args["deal_id"])

    @api.response(201, 'vote successfully created.')
    @api.doc('create a new vote')
    @api.param('deal_id', "the deal id passed in")
    @api.param('stage', "the type of vote this is ('initial' or 'final')")
    @api.param('name', "the name of the person voting")
    @api.expect(_vote, validate=True)
    def post(self):
        """Creates a new vote """
        parser = reqparse.RequestParser()
        parser.add_argument("stage", type=str)
        parser.add_argument("deal_id", type=int)
        parser.add_argument("name", type=str)
        args = parser.parse_args()
        data = request.json
        return save_new_vote(args["deal_id"], args["stage"], args["name"], data=data)

@api.route('/<vote_id>')
@api.param('vote_id', 'The vote identifier')
@api.response(404, 'Vote not found.')
class Vote(Resource):
    @api.doc('get a vote')
    @api.marshal_with(_vote)
    def get(self, vote_id):
        """get a vote given its identifier"""
        vote = get_a_vote(vote_id)
        if not vote:
            api.abort(404)
        else:
            return vote