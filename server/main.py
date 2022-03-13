from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from dotenv import dotenv_values
from werkzeug.utils import secure_filename
import fiona
import geopandas as gpd
import os
from uuid import uuid4

from database import Connection
import functions as func
import raster as rst


app = Flask(__name__)
CORS(app)  # , expose_headers='Authorization'

user_id = uuid4()
root_dir = os.path.abspath(os.getcwd())

# app['UPLOAD_DIR'] = os.path.join(root_dir, "/upload")
# app['DOWNLOAD_DIR'] = os.path.join(root_dir, "/download")

try:
    config = dotenv_values(".env")

    pg_user = config.get("PG_USER")
    pg_host = config.get("PG_HOST")
    pg_password = config.get("PG_PASSWORD")
    pg_db = config.get("PG_DB")

    db = Connection(pg_host, pg_db, pg_user, pg_password)

except Exception as e:
    app.logger.error(e)
    db = None


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
    return "Under construction"


@app.route('/download', methods=['POST'])
@cross_origin()
def download():
    return "Under construction"


if __name__ == '__main__':
    app.run()
