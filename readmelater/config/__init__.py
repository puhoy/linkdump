class Config(object):
    DEBUG = True
    TESTING = False
    DATABASE_URI = 'sqlite:///:memory:'


from .development import DevelopmentConfig
from .production import ProductionConfig
from .testing import TestingConfig



environments = dict(
    development=DevelopmentConfig,
    production=ProductionConfig,
    testing=TestingConfig
)


