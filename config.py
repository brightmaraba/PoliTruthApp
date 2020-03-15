import os
class Config:
    DEBUG = False

    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://ptadbadmin:5114@localhost:5432/ptadb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.environ.get('SECRET_KEY')
    JWT_ERROR_MESSAGE_KEY = 'message'

    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']

    UPLOADED_IMAGES_DEST = 'static/images'

    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 10 * 60

    RATE_LIMIT_HEADERS_ENABLED = True
