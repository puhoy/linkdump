from dramatiq.brokers.redis import RedisBroker

from linkdump.config import Config
import os


class DevelopmentConfig(Config):
    os.environ['FLASK_DEBUG'] = '1'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DEBUG = True
    
    SECRET_KEY = 'secret'

    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:secret@db/development'

    SERVER_NAME = 'localhost:8080'
    BASE_URL = 'http://localhost:8080/'
    DRAMATIQ_BROKER = RedisBroker
    DRAMATIQ_BROKER_URL = 'redis://redis/'

    MAIL_SERVER = 'smtp.example.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'username'
    MAIL_PASSWORD = 'password'
    SECURITY_TRACKABLE = True

    # https://pythonhosted.org/Flask-Security/configuration.html
    SECURITY_REGISTERABLE = True
    SECURITY_CONFIRMABLE = False  # disable email verification
    SECURITY_PASSWORD_SALT = 'salt!'

    SECURITY_LOGIN_URL = '/login'
    SECURITY_LOGOUT_URL = '/logout'
    SECURITY_REGISTER_URL = '/register'
    SECURITY_RESET_URL = '/reset'
    SECURITY_CHANGE_URL = '/change'
    SECURITY_CONFIRM_URL = '/confirm'
    SECURITY_POST_LOGIN_VIEW = '/'
    SECURITY_POST_LOGOUT_VIEW = '/'

