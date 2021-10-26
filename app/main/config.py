import os

# uncomment the line below for postgres database url from environment variable
#postgres_local_base = "postgresql://ycsmaqlgqyyaqa:2495c588708c88d2f499eace3e87154ed41182ff9ddbf0629c37378c051e67c8@ec2-34-225-167-77.compute-1.amazonaws.com:5432/d8vbbk7ngpk3ql"

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'my_precious_secret_key'
    #SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    DEBUG = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'tryrenta@gmail.com'
    MAIL_PASSWORD = 'vgnpapuiolnsgtoi'
    SECURITY_PASSWORD_SALT = 'my_precious_two'

class DevelopmentConfig(Config):
    # uncomment the line below to use postgres
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'flask_boilerplate_test.db')
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'flask_boilerplate_main.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'flask_boilerplate_test.db')
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    # uncomment the line below to use postgres
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'flask_boilerplate_test.db')


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY