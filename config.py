class Config(object):
    DEBUG = False
    TESTING = False
    # CSRF_ENABLED = True
    SECRET_KEY = 'SOMETHIN-RANDOM'
    SESSION_COOKIE_NAME = 'spotify-api'
    TOKEN_INFO = 'token_info'

class DevelopmentConfig(Config):
    ENV="development"
    DEVELOPMENT=True
    DEBUG=True
    