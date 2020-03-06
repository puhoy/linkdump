import os

from dramatiq.brokers.redis import RedisBroker

from linkdump.config import Config


class DefaultConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False

    DRAMATIQ_BROKER = RedisBroker

    SECURITY_LOGIN_URL = '/login'
    SECURITY_LOGOUT_URL = '/logout'
    SECURITY_REGISTER_URL = '/register'
    SECURITY_RESET_URL = '/reset'
    SECURITY_CHANGE_URL = '/change'
    SECURITY_CONFIRM_URL = '/confirm'
    SECURITY_POST_LOGIN_VIEW = '/'
    SECURITY_POST_LOGOUT_VIEW = '/'
