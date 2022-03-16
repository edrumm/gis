from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from dotenv import dotenv_values
from werkzeug.utils import secure_filename
import fiona
import geopandas as gpd
import os, sys, signal
from uuid import uuid4
from sqlalchemy import create_engine

from database import Connection
import functions as func
import raster
import file


app = Flask(__name__)
CORS(app, expose_headers='Authorization')

user_id = uuid4()
root_dir = os.path.abspath(os.getcwd())

app.config['UPLOAD_DIR'] = os.path.join(root_dir, "/upload")
app.config['DOWNLOAD_DIR'] = os.path.join(root_dir, "/download")
app.config['SUPPORTED_TYPES'] = [".shp", ".zip", ".geojson", ".bil", ".tif"]

try:
    config = dotenv_values(".env")

    pg_user = config.get("PG_USER")
    pg_host = config.get("PG_HOST")
    pg_password = config.get("PG_PASSWORD")
    pg_db = config.get("PG_DB")
    pg_port = 5432

    db = Connection(pg_host, pg_db, pg_user, pg_password, pg_port)

except Exception as e:
    app.logger.error(e)
    db = None

if not os.path.isdir(app.config['UPLOAD_DIR']):
    os.mkdir(app.config['UPLOAD_DIR'])

if not os.path.isdir(app.config['DOWNLOAD_DIR']):
    os.mkdir(app.config['DOWNLOAD_DIR'])


@app.route('/', methods=['GET'])
def main():
    return "127.0.0.1:5000"


@app.route('/convex', methods=['POST'])
@cross_origin()
def convex_hull():
    req = request.json

    try:
        geom = func.convex_hull(db, req['points'])

        return jsonify({
            'body': geom.to_json(),
            'layer': None,
            'err': None
        })

    except Exception as err:
        return jsonify({
            'body': None,
            'layer': None,
            'err': str(err)
        })


@app.route('/voronoi', methods=['POST'])
@cross_origin()
def voronoi_polygons():
    req = request.json

    try:
        geom = func.voronoi_polygons(db, req['points'])

        return jsonify({
            'body': geom.to_json(),
            'layer': None,
            'err': None
        })

    except Exception as err:
        return jsonify({
            'body': None,
            'layer': None,
            'err': str(err)
        })


@app.route('/count', methods=['POST'])
@cross_origin()
def count():
    req = request.json

    try:
        geom = func.count_points_in_polygon(db, req['polygon'], req['points'])

        return jsonify({
            'body': geom.to_json(),
            'layer': None,
            'err': None
        })

    except Exception as err:
        return jsonify({
            'body': None,
            'layer': None,
            'err': str(err)
        })


@app.route('/raster', methods=['POST'])
@cross_origin()
def rasterize():
    return "Under construction"


@app.route('/polygon', methods=['POST'])
@cross_origin()
def polygonize():
    return "Under construction"


@app.route('/slope', methods=['POST'])
@cross_origin()
def slope():
    return "Under construction"


@app.route('/aspect', methods=['POST'])
@cross_origin()
def aspect():
    return "Under construction"


@app.route('/test', methods=['GET', 'POST'])
@cross_origin()
def test():
    try:
        geom = func.count_points_in_polygon(db, 'nyc_neighborhoods', 'nyc_homicides')

        return jsonify({
            'body': geom.to_json(),
            'layer': None,
            'err': None
        })

    except Exception as err:
        return jsonify({
            'body': None,
            'layer': None,
            'err': str(err)
        })

    # return func.convex_hull(db, 'nyc_subway_stations').to_json()
    # return func.voronoi_polygons(db, 'nyc_subway_stations').to_json()


@app.route('/upload', methods=['POST'])
@cross_origin()
def upload():
    try:
        f = request.files['file']

        if not any(ext in f.filename for ext in app.config['SUPPORTED_TYPES']):
            raise IOError("The uploaded file type is not supported")

        filename = secure_filename(f.filename)
        layer_name = f.filename.partition('.')[0]
        path = os.path.join(app.config['UPLOAD_DIR'], filename)
        f.save(path)

        geom = file.read_vector(path)
        db.postgis_insert(geom, layer_name, 26918)

        return jsonify({
            'body': geom.to_json(),
            'layer': layer_name,
            'err': None
        })

    except Exception as e:
        return jsonify({
            'body': None,
            'layer': None,
            'err': str(e)
        })


@app.route('/download', methods=['POST'])
@cross_origin()
def download():
    return "Under construction"


def stop():
    sys.exit(0)


if __name__ == '__main__':
    app.run()
