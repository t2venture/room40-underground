from flask import request
from flask_restplus import Resource, reqparse

from ..util.dto import VoteDto
from ..service.vote_service import save_new_vote, get_all_votes, get_a_vote, update_vote, delete_a_vote

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
    @api.expect(_vote, validate=True)
    def post(self):
        """Creates a new vote """
        data = request.json
        return save_new_vote(data=data)

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

    @api.response(201, 'vote successfully created.')
    @api.doc('update a vote')
    @api.expect(_vote, validate=True)
    def put(self, vote_id):
        """Update a vote """
        data = request.json
        return update_vote(vote_id, data)

    @api.response(201, 'vote successfully deleted.')
    @api.doc('delete a vote')
    def delete(self, vote_id):
        """Delete a vote """
        return delete_a_vote(vote_id)
    