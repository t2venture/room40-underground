from flask import request
from flask_restplus import Resource, reqparse

from ..util.dto import DocumentDto
from ..service.document_service import save_new_document, get_all_documents, get_a_document, update_document, \
    delete_a_document
from ..service.auth_helper import Auth
import json
import datetime
from ..util.decorator import token_required, admin_token_required

api = DocumentDto.api
_document = DocumentDto.document


@api.route('/')
class DocumentList(Resource):
    @api.doc('list_of_documents for a document')
    @api.marshal_list_with(_document, envelope='data')
    @api.param("title", "title of the document")
    @api.param("is_deleted", "whether the document is deleted")
    @api.param("is_active", "whether the document is active")
    def get(self):
	    '''List all documents'''
	    parser = reqparse.RequestParser()
	    parser.add_argument("title", type=str)
	    parser.add_argument("is_deleted", type=bool)
	    parser.add_argument("is_active", type=bool)
	    args = parser.parse_args()
	    return get_all_documents(args["title"], args["is_deleted"], args["is_active"])

    @api.response(201, 'Document successfully created.')
    @api.doc('create a new document')
    @api.expect(_document, validate=True)
    @admin_token_required
    def post(self):
	    """Creates a new Document """
	    data = request.json
	    logined, status = Auth.get_logged_in_user(request)
	    token=logined.get('data')
	    if not token:
		    return logined, status
	    login_user={"login_user_id": token['user_id']}
	    action_time={"action_time": datetime.datetime.utcnow()}
	    data.update(login_user)
	    data.update(action_time)	    
	    return save_new_document(data=data)


@api.route('/<document_id>')
@api.param('document_id', 'The Document identifier')
@api.response(404, 'Document not found.')
class Document(Resource):
    @api.doc('get a document')
    @api.marshal_with(_document)
    def get(self, document_id):
        """get a document given its identifier"""
        document = get_a_document(document_id)
        if not document:
            api.abort(404)
        else:
            return document

    @api.response(201, 'document successfully updated.')
    @api.doc('update a document')
    @api.expect(_document, validate=True)
    @admin_token_required
    def put(self, document_id):
	    """Update a document"""
	    data = request.json
	    logined, status = Auth.get_logged_in_user(request)
	    token=logined.get('data')
	    if not token:
		    return logined, status
	    login_user={"login_user_id": token['user_id']}
	    action_time={"action_time": datetime.datetime.utcnow()}
	    data.update(login_user)
	    data.update(action_time)
	    return update_document(document_id, data)

    @api.response(201, 'document successfully deleted.')
    @api.doc('delete a document')
    @admin_token_required
    def delete(self, document_id):
	    """Delete a document"""
	    logined, status = Auth.get_logged_in_user(request)
	    token=logined.get('data')
	    if not token:
		    return logined, status
	    data=dict()
	    login_user={"login_user_id": token["user_id"]}
	    action_time={"action_time": datetime.datetime.utcnow()}
	    data.update(login_user)
	    data.update(action_time)
	    return delete_a_document(document_id, data)