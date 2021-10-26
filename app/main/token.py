from itsdangerous import URLSafeTimedSerializer

import app


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])
	

def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer('secret_key')
    try:
        email = serializer.loads(
            token,
            salt='my_precious_salt',
            max_age=expiration
        )
    except:
        return False
    return email