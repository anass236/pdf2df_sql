import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(os.getcwd(), '.env'))

SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
SQLALCHEMY_ENGINE_OPTIONS = {'ssl': {'ca': './creds/ca-certificate.crt'}}  # Optional for SSL connections
