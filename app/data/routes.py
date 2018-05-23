import ast
import sys
import psycopg2

from flask import jsonify, current_app, request
from app.data import bp

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
    # connect to the database
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
    # query with help from https://gis.stackexchange.com/questions/112057/
    # sql-query-to-have-a-complete-geojson-feature-from-postgis/191446#191446
    query = """
SELECT jsonb_build_object(
    'type',         'FeatureCollection',
    'features',     jsonb_agg(features)
)
FROM (
    SELECT jsonb_build_object(
        'type',         'Feature',
        'id',           id,
        'geometry',     ST_AsGeoJSON(geom)::jsonb,
        'properties',   to_jsonb(inputs) - 'id' - 'geom'
    ) AS feature
    FROM (
        SELECT *
        FROM provincies
        WHERE provincies.geom && ST_MakeEnvelope({0}, {1}, {2}, {3}, 4326)
        ) inputs) features;""".format(xmin, ymin, xmax, ymax)

    cursor.execute(query)

    data = cursor.fetchone()

    return jsonify(data)
