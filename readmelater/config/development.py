from dramatiq.brokers.redis import RedisBroker

from readmelater.config import Config
import os


class DevelopmentConfig(Config):
    os.environ['FLASK_DEBUG'] = '1'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:secret@localhost/development'

    BASE_URL = 'http://localhost:5000/'
    DRAMATIQ_BROKER = RedisBroker