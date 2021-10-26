from itsdangerous import URLSafeTimedSerializer


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer('secret_key')
    return serializer.dumps(email, salt='my_precious_salt')
	

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