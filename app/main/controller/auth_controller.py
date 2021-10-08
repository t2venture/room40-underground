from flask import request
from flask_restplus import Resource
import datetime
from app.main.service.user_service import save_new_user
from app.main.service.auth_helper import Auth
from ..util.dto import AuthDto
from ..util.dto import UserDto
api = AuthDto.api
user_auth = AuthDto.user_auth

@api.route('/login')
class UserLogin(Resource):
    """
        User Login Resource
    """
    @api.doc('user login')
    @api.expect(user_auth, validate=True)
    def post(self):
        # get the post data
        post_data = request.json
        return Auth.login_user(data=post_data)


@api.route('/signup')
class SignupAPI(Resource):
    '''
    Signup Resource
    '''
    @api.response(201, 'User successfully created.')
    @api.doc('signup a user')
    def post(self):
        """Creates a new User """
        data = request.json
        action_time={"action_time": datetime.datetime.utcnow()}
        data.update(action_time)	
        return save_new_user(data=data)

@api.route('/logout')
class LogoutAPI(Resource):
    """
    Logout Resource
    """
    @api.doc('logout a user')
    def post(self):
        # get auth token
        auth_header = request.headers.get('Authorization')
        return Auth.logout_user(data=auth_header)