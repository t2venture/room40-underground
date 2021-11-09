from flask import request
from flask_restplus import Resource, reqparse

from ..util.dto import UserDto
from ..service.user_service import save_new_user, get_all_users, get_a_user, update_user, delete_a_user, check_same_company
from ..service.auth_helper import Auth
import datetime
import json
from ..util.decorator import token_required, admin_token_required
api = UserDto.api
_user = UserDto.user


@api.route('/')
class UserList(Resource):
    @api.doc('list_of_registered_users')
    @api.param('is_deleted', 'whether the user is deleted')
    @api.param('is_active', 'whether the user is active')
    @api.marshal_list_with(_user, envelope='data')
    @token_required
    def get(self):
        """List all registered users"""
        parser = reqparse.RequestParser()
        parser.add_argument("is_deleted", type=bool)
        parser.add_argument("is_active", type=bool)
        args = parser.parse_args()
        logined, status = Auth.get_logged_in_user(request)
        token=logined.get('data')
        if not args['is_deleted']:
            args['is_deleted']=False
        if not args['is_active']:
            args['is_active']=True
        if token['admin']==False:
            adm=False
            usr=int(token['user_id'])
        else:
            adm=True
            usr=1
        return get_all_users(args['is_deleted'], args['is_active'], adm, usr)

    @api.response(201, 'User successfully created.')
    @api.doc('create a new user')
    @api.expect(_user, validate=True)
    def post(self):
        """Creates a new User """
        data = request.json
        action_time={"action_time": datetime.datetime.utcnow()}
        data.update(action_time)	
        return save_new_user(data=data)


@api.route('/<user_id>')
@api.param('user_id', 'The User identifier')
@api.response(404, 'User not found.')
class User(Resource):
    @api.doc('get a user')
    @api.marshal_with(_user)
    @token_required
    def get(self, user_id):
        """get a user given its identifier"""
        user = get_a_user(user_id)
        logined, status = Auth.get_logged_in_user(request)
        #You can check user information for other IDs (as non admin) if same company.
        token=logined.get('data')
        if not token:
            return logined, status
        if token['admin']==False and user_id!=token['user_id']:
            response_object = {
                'status': 'fail',
                'message': 'You cannot search for this information.'
                }
            return response_object, 401
        if not user:
            api.abort(404)
        else:
            return user

    @api.response(201, 'user successfully updated.')
    @api.doc('update a user')
    @api.expect(_user, validate=True)
    @token_required
    def put(self, user_id):
        """Update a user """
        data = request.json
        action_time={"action_time": datetime.datetime.utcnow()}
        data.update(action_time)
        logined, status = Auth.get_logged_in_user(request)
        token=logined.get('data')
        if not token:
            return logined, status
        token['user_id']=int(token['user_id'])
        user_id=int(user_id)
        print (token['admin'])
        print (user_id, type(user_id))
        print (token['user_id'], type(token['user_id']))
        if token['admin']==False:
            if user_id and user_id!=token['user_id']:
                response_object = {
                    'status': 'fail',
                    'message': 'You cannot update this information.'
                    }
                return response_object, 401
        if token['admin']==False and 'password' in data.keys():
            del data['password']
        login_user={"login_user_id": token['user_id']}
        data.update(login_user)
        return update_user(user_id, data)

    @api.response(201, 'user successfully deleted.')
    @api.doc('delete a user')
    @token_required
    def delete(self, user_id):
        """Delete a user """
        logined, status = Auth.get_logged_in_user(request)
        token=logined.get('data')
        if not token:
            return logined, status
        if token['admin']==False:
            if user_id!=token['user_id']:
                response_object = {
                    'status': 'fail',
                    'message': 'You cannot delete this information.'
                    }
                return response_object, 401
        data=dict()
        login_user={"login_user_id": token["user_id"]}
        action_time={"action_time": datetime.datetime.utcnow()}
        data.update(login_user)
        data.update(action_time)
        return delete_a_user(user_id, data)