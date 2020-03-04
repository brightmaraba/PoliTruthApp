class Config:
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://ptadbadmin:5114@localhost/ptadb'
    SQL_ALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = 'super-secret-key'
    JWT_ERROR_MESSAGE = 'message'

    JWT_BLACKLIST_ENABLED = True
    JWT_BLACK_LIST_TOKEN_CHECKS = ['access', 'refresh']
