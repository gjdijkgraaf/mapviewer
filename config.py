import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dummy-key-you-wont-guess'
    DATABASE_CONN_STRING = os.environ.get('DATABASE_CONN_STRING') or \
        "dbname='gerritjandijkgraaf' user='gerritjandijkgraaf' host='localhost' password=''"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://gerritjandijkgraaf:@localhost:5432/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
