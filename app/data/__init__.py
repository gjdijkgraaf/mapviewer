from flask import Blueprint
from app.data.queries import PostgreSQLQueries

bp = Blueprint('data', __name__)
queries = PostgreSQLQueries()

from app.data import routes
