import os

class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'mysecretkey')

class ProductionConfig(Config):
    DATABASE_URI = 'postgresql://postgres:123456789@localhost/BD_ArtesGraficas'

class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URI = 'postgresql://postgres:123456789@localhost/BD_ArtesGraficas'

class TestingConfig(Config):
    TESTING = True
    DATABASE_URI = 'postgresql://postgres:123456789@localhost/BD_ArtesGraficas'

config = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig
}