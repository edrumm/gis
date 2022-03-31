from flask import Flask, jsonify, request, send_file
from flask_cors import CORS, cross_origin
from dotenv import dotenv_values
from werkzeug.utils import secure_filename
from uuid import uuid4
from database import Connection
import geopandas as gpd
import os, zipfile
import file, functions, raster, crs


app = Flask(__name__)
CORS(app, expose_headers='Authorization')

user_id = uuid4()
root_dir = os.path.abspath(os.getcwd())


def dir_config(tag):
    if not os.path.exists(app.config[tag]):
        os.mkdir(app.config[tag])
    else:
        filelist = [f for f in os.listdir(app.config[tag])]
        for f in filelist:
            os.remove(os.path.join(app.config[tag], f))


def generate_file_num():
    num = 0

    while True:
        yield num
        num += 1


file_num = generate_file_num()

app.config['UPLOAD_DIR'] = os.path.join(root_dir, "/upload")
app.config['DOWNLOAD_DIR'] = os.path.join(root_dir, "/download")
app.config['SUPPORTED_TYPES'] = [".shp", ".zip", ".geojson", ".bil", ".tif"]

user_upload_dir = os.path.join(app.config['UPLOAD_DIR'], str(user_id))
user_download_dir = os.path.join(app.config['DOWNLOAD_DIR'], str(user_id))

dir_config('UPLOAD_DIR')
dir_config('DOWNLOAD_DIR')

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


def extract_zip(path):
    with zipfile.ZipFile(path, "r") as z:
        z.extractall(path)


def create_zip(paths, zip_path):
    with zipfile.ZipFile(zip_path, "w") as z:
        for path in paths:
            z.write(path)


@app.route('/', methods=['GET'])
def main():
    return jsonify({
        'db': True if db else False,
        'uuid': user_id,
        'root_dir': root_dir,
        'upload_dir': app.config['UPLOAD_DIR'],
        'download_dir': app.config['DOWNLOAD_DIR'],
        'supported_types': app.config['SUPPORTED_TYPES']
    })


@app.route('/convex', methods=['POST'])
@cross_origin()
def convex_hull():
    req = request.json

    try:
        geom = functions.convex_hull(db, req['points'])
        geom = crs.to_web_mercator(geom)

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
        geom = functions.voronoi_polygons(db, req['points'])
        geom = crs.to_web_mercator(geom)

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
        geom = functions.count_points_in_polygon(db, req['polygon'], req['points'])
        geom = crs.to_web_mercator(geom)

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


@app.route('/slope', methods=['POST'])
@cross_origin()
def slope():
    try:
        path = os.path.join(app.config['UPLOAD_DIR'], request.json['file'])
        ds = raster.get_gdal_dataset(path)

        filename = request.json['file'].partition('.')[0] + next(file_num)

        slp = raster.aspect(ds, os.path.join(app.config['DOWNLOAD_DIR'], f'{filename}.tif'))
        raster.write_raster(slp, os.path.join(app.config['DOWNLOAD_DIR'], f'{filename}.png'))

        return jsonify({
            'body': True,
            'layer': 'slope',
            'err': None
        })

    except Exception as e:
        return jsonify({
            'body': None,
            'err': str(e)
        })


@app.route('/aspect', methods=['POST'])
@cross_origin()
def aspect():
    try:
        path = os.path.join(app.config['UPLOAD_DIR'], request.json['file'])
        ds = raster.get_gdal_dataset(path)

        filename = request.json['file'].partition('.')[0] + next(file_num)

        asp = raster.aspect(ds, os.path.join(app.config['DOWNLOAD_DIR'], f'{filename}.tif'))
        raster.write_raster(asp, os.path.join(app.config['DOWNLOAD_DIR'], f'{filename}.png'))

        return jsonify({
            'body': True,
            'layer': 'aspect',
            'err': None
        })

    except Exception as e:
        return jsonify({
            'body': None,
            'err': str(e)
        })


@app.route('/test', methods=['GET', 'POST'])
@cross_origin()
def test():
    try:
        geom = functions.count_points_in_polygon(db, 'nyc_neighborhoods', 'nyc_homicides')
        geom = crs.to_web_mercator(geom)

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


@app.route('/drop', methods=['POST'])
@cross_origin()
def drop():
    try:
        db.postgis_drop_layer(request.json['layer'])

        return jsonify({
            'body': True,
            'err': None
        })

    except Exception as e:
        return jsonify({
            'body': None,
            'err': str(e)
        })


@app.route('/upload', methods=['POST'])
@cross_origin()
def upload():
    try:
        f = request.files['file']

        if not any(ext in f.filename for ext in app.config['SUPPORTED_TYPES']):
            raise IOError("The uploaded file type is not supported")

        elif ".shp" in f.filename:
            raise IOError("A shapefile must be uploaded as a zip with required supplementary files and optional prj")

        filename = secure_filename(f.filename)
        layer_name = f.filename.partition('.')[0]
        path = os.path.join(app.config['UPLOAD_DIR'], filename)
        f.save(path)

        if ".tif" in filename:
            return jsonify({
                'body': True,
                'layer': layer_name,
                'err': None
            })

        else:
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
    try:
        return jsonify({
            'body': "Under construction",
            'err': None
        })

    except Exception as e:
        return jsonify({
            'body': None,
            'err': str(e)
        })


if __name__ == '__main__':
    app.run()
