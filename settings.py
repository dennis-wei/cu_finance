import os

ENVIRONMENT = os.getenv('ENVIRONMENT', 'local')

DATABASE_NAME = os.getenv('DATABASE_NAME', 'finance_db')
DATABASE_HOST = os.getenv('DATABASE_HOST', 'localhost')
DATABASE_PORT = os.getenv('DATABASE_PORT', 5432)
DATABASE_USER = os.getenv('DATABASE_USER', 'dennis')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD', '')

SQLALCHEMY_DATABASE_URI = 'postgresql://%s:%s@%s:%s/%s' % (
    DATABASE_USER,
    DATABASE_PASSWORD,
    DATABASE_HOST,
    DATABASE_PORT,
    DATABASE_NAME
)
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = 'passwordgoeshere'
WTF_CSRF_ENABLED = True

USERNAME = 'admin@coreatcu.com'
PASSWORD = 'admin'

BASE_ALLOCATION = 3520.17
