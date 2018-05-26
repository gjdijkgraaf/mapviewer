import ast
import sys
import psycopg2

from flask import jsonify, current_app, request
from app.data import bp
from app.data import queries
from app.data.checks import is_number

@bp.route('/fetch/<layer>', methods=['GET', 'POST'])
def fetch(layer):
    data = {1: {'type': 'Feature',
                'geometry': {'type': 'Point',
                             'coordinates': [6.1, 52.516667]},
                'properties': {'Hoofdstad': 'Zwolle',
                               'Provincie': 'Overijssel'}},
            2: {'type': 'Feature',
                'geometry': {'type': 'Point',
                             "coordinates": [5.916667, 51.983333]},
                'properties': {'Hoofdstad': 'Arnhem',
                               'Provincie': 'Gelderland'}}}

    return jsonify(data[int(layer)])

@bp.route('/data/<layer>', methods=['GET', 'POST'])
def data(layer):
    # set crs
    crs = 4326

    # get layer properties (eventually from system database)
    if int(layer) == 1:
        tablename = 'provincies'
        geometry_column = 'geom'
        id_column = 'id'
    elif int(layer) == 2:
        tablename = ' gemeentehuizen'
        geometry_column = ' geom'
        id_column = 'id'

    # connect to the data database
    try:
        conn = psycopg2.connect(current_app.config['DATABASE_CONN_STRING'])
        cursor = conn.cursor()
    except:
        print("Unexpected error: ", sys.exc_info()[0])
        raise

    # get the bounding box
    xmin = request.args.get('xmin')
    ymin = request.args.get('ymin')
    xmax = request.args.get('xmax')
    ymax = request.args.get('ymax')
    # verify the inputs to prevent SQL injection
    if is_number(xmin) and is_number(ymin) and is_number(xmax) and is_number(ymax):
        query = queries.postgresql_fetch_bbox.format(
            id_column, geometry_column, tablename, xmin, ymin, xmax, ymax, crs)
        cursor.execute(query)
        data = cursor.fetchone()
    else:
        data = ""

    return jsonify(data)
