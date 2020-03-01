from readmelater.config import Config


class DevelopmentConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'
