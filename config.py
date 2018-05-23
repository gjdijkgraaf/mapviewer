import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DATABASE_CONN_STRING = os.environ.get('DATABASE_CONN_STRING') or \
        "dbname='gerritjandijkgraaf' user='gerritjandijkgraaf' host='localhost' password=''"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'mapviewer.db')
