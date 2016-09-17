import os

ENVIRONMENT = os.getenv('ENVIRONMENT', 'local')

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.getenv('DATA_DIR', os.path.join(BASE_DIR, "data"))
EXPEND_DIR = os.getenv('EXPEND_DIR', os.path.join(DATA_DIR, "expenditure"))
REVEN_DIR =os.getenv('REVEN_DIR', os.path.join(DATA_DIR, "revenue"))

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
