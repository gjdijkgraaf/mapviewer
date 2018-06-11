import ast
import sys
import psycopg2

from flask import jsonify, current_app, request
from flask_login import current_user
from app.data import bp
from app.data import queries
from app.data.checks import is_number
from app.models import Layer, Project


@bp.route('/data/<tablename>', methods=['GET', 'POST'])
def data(tablename):
    # check if user is allowed to access this data
    ## to be implemented ##
    project_id = request.args.get('project_id')
    project = Project.query.get(project_id)
    if current_user not in project.users:
        return jsonify("")

    # set crs
    crs = 4326

    # get layer properties
    layer = Layer.query.filter_by(tablename=tablename).first()
    geometry_column = layer.geometry_column
    id_column = layer.id_column

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

@bp.route('/list_tables', methods=['GET', 'POST'])
def list_tables():
    try:
        conn = psycopg2.connect(current_app.config['DATABASE_CONN_STRING'])
        cursor = conn.cursor()
    except:
        print("Unexpected error: ", sys.exc_info()[0])
        raise

    query = queries.postgresql_list_tables
    cursor.execute(query)
    data = [row for row in cursor if not row[0] in current_app.config['IGNORE_TABLE_NAMES']]

    return jsonify(data)
