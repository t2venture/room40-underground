from flask import request
from flask_restplus import Resource, reqparse

from ..util.dto import AssessmentDto
from ..service.assessment_service import save_new_assessment, get_all_assessments, get_a_assessment, update_assessment, delete_a_assessment

api = AssessmentDto.api
_assessment = AssessmentDto.assessment


@api.route('/')
class AssessmentList(Resource):
    @api.doc('list_of_assessments for a company')
    @api.param('company_id', 'The company identifier')
    @api.marshal_list_with(_assessment, envelope='data')
    def get(self):
        """List all assessments"""
        parser = reqparse.RequestParser()
        parser.add_argument("company_id", type=int)
        args = parser.parse_args()
        return get_all_assessments(args['company_id'])

    @api.response(201, 'assessment successfully created.')
    @api.doc('create a new assessment')
    @api.expect(_assessment, validate=True)
    def post(self):
        """Creates a new assessment """
        data = request.json
        return save_new_assessment(data=data)

@api.route('/<assessment_id>')
@api.param('assessment_id', 'The assessment identifier')
@api.response(404, 'assessment not found.')
class Assessment(Resource):
    @api.doc('get an assessment')
    @api.marshal_with(_assessment)
    def get(self, assessment_id):
        """get a user given its identifier"""
        assessment = get_a_assessment(assessment_id)
        if not assessment:
            api.abort(404)
        else:
            return assessment

    @api.response(201, 'assessment successfully created.')
    @api.doc('update a assessment')
    @api.expect(_assessment, validate=True)
    def put(self, assessment_id):
        """Update a assessment """
        data = request.json
        return update_assessment(assessment_id, data)

    @api.response(201, 'assessment successfully deleted.')
    @api.doc('delete a assessment')
    def delete(self, assessment_id):
        """Delete a assessment """
        return delete_a_assessment(assessment_id)