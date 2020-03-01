from readmelater.config import Config


class ProductionConfig(Config):
    DEBUG = False
    DATABASE_URI = 'sqlite:///prod.db'
