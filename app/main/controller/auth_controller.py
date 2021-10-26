from flask import request
from flask_restplus import Resource, reqparse
import datetime
from app.main.service.user_service import save_new_user, check_if_registered_user, get_a_user_by_email, update_user, send_change_password_email
from app.main.service.auth_helper import Auth
from ..util.dto import AuthDto
from ..util.dto import UserDto
from ..util.email import set_password, send_confirmation_email, send_change_password_email
from app.main.token import generate_confirmation_token, confirm_token

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

@api.route('/forgotpassword')
class ForgotPasswordAPI(Resource):
    '''
    Forgot Password Resource
    '''
    @api.response('200', 'An email has been sent with the temporary password. Please login and change your password')
    @api.param('email_address', 'your email address')
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("email_address", type=str)
        args=parser.parse_args()
        flag=check_if_registered_user(args['email_address'])
        if flag==False:
            response_object = {
            'status': 'fail',
            'message': 'Your email address is not registered.'}
            return response_object, 401
        else:
            #METHOD 1
            ####
            '''
            new_password=set_password()
            changed_user=get_a_user_by_email(args['email_address'])
            id_changed_user=changed_user["id"]
            data=dict()
            data['login_user_id']=1
            data['action_time']=datetime.datetime.utcnow()
            data['password']=new_password
            update_user(id_changed_user, data)
            ##SEND EMAIL FUNCTION
            send_change_password_email(args['email_address'], new_password)
            '''
            ###
            #METHOD 2 (MORE SECURE)
            ###
            confirmation_token=generate_confirmation_token(args["email_address"])
            response_object={
                'status': 'success',
                'message': 'Successfully registered. Please confirm your email.',
                'confirmation': confirmation_token
            }
            return response_object, 201
            ###
            


