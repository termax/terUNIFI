import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = \
        '\xcfA\xa2\xb52$*:c\xc2},E\x0f"\xb7\xc6\xc3\x1di\xc2\t\x93\xe6'
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = \
        'sqlite:///' + os.path.join(basedir, 'terunifi.db')
    REDIS_URL = 'redis://localhost:6379'
    REDIS_DATABASE=5


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
    WTF_CSRF_ENABLED = False
    SERVER_NAME = "localhost"


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = \
     'sqlite:///' + os.path.join(basedir, 'terunifi.db')


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)
