from flask import request
from flask_restplus import Resource

from ..util.dto import AssessmentDto
from ..service.assessment_service import save_new_assessment, get_all_assessments, get_a_assessment

api = AssessmentDto.api
_assessment = AssessmentDto.assessment


@api.route('/')
class AssessmentList(Resource):
    @api.doc('list_of_assessments for a company')
    @api.marshal_list_with(_assessment, envelope='data')
    def get(self, company_id):
        """List all assessments for a company"""
        return get_all_assessments(company_id)

    @api.response(201, 'assessment successfully created.')
    @api.doc('create a new assessment')
    @api.expect(_assessment, validate=True)
    def post(self, company_id):
        """Creates a new assessment """
        data = request.json
        return save_new_assessment(company_id, data=data)

@api.route('/<assessment_id>')
@api.param('company_id', 'The Company identifier')
@api.param('assessment_id', 'The assessment identifier')
@api.response(404, 'assessment not found.')
class Assessment(Resource):
    @api.doc('get an assessment')
    @api.marshal_with(_assessment)
    def get(self, company_id, assessment_id):
        """get a user given its identifier"""
        assessment = get_a_assessment(company_id, assessment_id)
        if not assessment:
            api.abort(404)
        else:
            return assessment