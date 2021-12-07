class Config(object):
    DEBUG = False
    TESTING = False
    # CSRF_ENABLED = True
    SECRET_KEY = 'SOMETHIN-RANDOM'


class DevelopmentConfig(Config):
    ENV="development"
    DEVELOPMENT=True
    DEBUG=True
    