from flask import Flask, jsonify, request, send_file, make_response
from flask_cors import CORS, cross_origin
from geojson_rewind import rewind
from dotenv import dotenv_values
from werkzeug.utils import secure_filename
from uuid import uuid4
from database import Connection
import geopandas as gpd
import os, zipfile, shutil
import file, functions, raster, crs


# ---------------- CONFIG STUFF ----------------

app = Flask(__name__)
CORS(app, expose_headers='Authorization')

user_id = uuid4()
root_dir = os.path.abspath(os.getcwd())


# Clean and build server file system
# For local use
def dir_config(path):
    user_path = os.path.join(path, str(user_id))

    if not os.path.exists(path):
        os.mkdir(path)

    else:
        filelist = [f for f in os.listdir(path)]
        for f in filelist:
            shutil.rmtree(os.path.join(path, f))

    os.mkdir(user_path)


# App config
app.config['UPLOAD_DIR'] = os.path.join(root_dir, "upload", str(user_id))
app.config['DOWNLOAD_DIR'] = os.path.join(root_dir, "download", str(user_id))
app.config['SUPPORTED_TYPES'] = [".shp", ".zip", ".geojson", ".tif"]

dir_config(os.path.join(root_dir, "upload"))
dir_config(os.path.join(root_dir, "download"))

# Connect to Postgres server
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


# ---------------- ZIPFILE IO ----------------

def extract_zip(path, output_path, name):
    output_path = os.path.join(output_path, name)
    os.mkdir(output_path)

    with zipfile.ZipFile(path, "r") as z:
        z.extractall(output_path)


def create_zip(paths, zip_path, name):
    zip_path = os.path.join(zip_path, name)

    with zipfile.ZipFile(zip_path, "w") as z:
        for path in paths:
            arcname = os.path.basename(path)
            z.write(path, arcname)


# ---------------- ROUTING SYSTEM ----------------

@app.route('/', methods=['GET'])
def main():
    return jsonify({
        'db': pg_db if db else None,
        'uuid': user_id,
        'root_dir': root_dir,
        'upload_dir': app.config['UPLOAD_DIR'],
        'download_dir': app.config['DOWNLOAD_DIR']
    })


@app.route('/convex', methods=['POST'])
@cross_origin()
def convex_hull():
    req = request.json

    try:
        geom = functions.convex_hull(db, req['points'])
        generate_file(f"{req['points']}-convexhull.geojson", frame=geom)

        geom = crs.to_WGS84(geom)
        geom = rewind(geom.to_json())

        return jsonify({
            'body': geom,
            'filename': f"{req['points']}-convexhull.geojson",
            'err': None
        })

    except Exception as err:
        return jsonify({
            'body': None,
            'err': str(err)
        })


@app.route('/voronoi', methods=['POST'])
@cross_origin()
def voronoi_polygons():
    req = request.json

    try:
        geom = functions.voronoi_polygons(db, req['points'])
        generate_file(f"{req['points']}-voronoipolygons.geojson", frame=geom)

        geom = crs.to_WGS84(geom)
        geom = rewind(geom.to_json())

        return jsonify({
            'body': geom,
            'filename': f"{req['points']}-voronoipolygons.geojson",
            'err': None
        })

    except Exception as err:
        return jsonify({
            'body': None,
            'err': str(err)
        })


@app.route('/count', methods=['POST'])
@cross_origin()
def count():
    req = request.json

    try:
        geom = functions.count_points_in_polygon(db, req['polygon'], req['points'])
        generate_file(f"points-in-{req['polygon']}.csv", frame=geom)

        geom = crs.to_WGS84(geom)
        geom = rewind(geom.to_json())

        return jsonify({
            'body': geom,
            'filename': f"points-in-{req['polygon']}.csv",
            'err': None
        })

    except Exception as err:
        return jsonify({
            'body': None,
            'err': str(err)
        })


@app.route('/slope', methods=['POST'])
@cross_origin()
def slope():
    try:
        path = os.path.join(app.config['UPLOAD_DIR'], request.json['file'])
        ds = raster.get_gdal_dataset(path)

        filename = request.json['file'].partition('.')[0]

        tif_path = os.path.join(app.config['DOWNLOAD_DIR'], f'{filename}.tif')
        png_path = os.path.join(app.config['DOWNLOAD_DIR'], f'{filename}.png')

        slp = raster.slope(ds, tif_path)
        raster.write_raster(slp, png_path)

        generate_file(f'{filename}.tif', alg="slope")

        response = make_response(send_file(png_path, mimetype="image/png"))
        response.headers["Content-Type"] = "image/png"
        return response

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

        filename = request.json['file'].partition('.')[0]

        tif_path = os.path.join(app.config['DOWNLOAD_DIR'], f'{filename}.tif')
        png_path = os.path.join(app.config['DOWNLOAD_DIR'], f'{filename}.png')

        asp = raster.aspect(ds, tif_path)
        raster.write_raster(asp, png_path)

        generate_file(f'{filename}.tif', alg="aspect")

        response = make_response(send_file(png_path, mimetype="image/png"))
        response.headers["Content-Type"] = "image/png"
        return response

    except Exception as e:
        return jsonify({
            'body': None,
            'err': str(e)
        })


@app.route('/test', methods=['GET', 'POST'])
@cross_origin()
def test():
    return jsonify({
        'body': "Test route",
        'err': None
    })


@app.route('/drop', methods=['POST'])
@cross_origin()
def drop():
    req = request.json

    try:
        path = os.path.join(app.config['UPLOAD_DIR'], req['filename'])
        os.remove(path)

        if ".tif" in req['filename']:
            return jsonify({
                'body': True,
                'err': None
            })

        table = req['filename'].partition('.')[0]

        if ".zip" in req['filename']:
            path = os.path.join(app.config['UPLOAD_DIR'], req['filename'])
            shutil.rmtree(path)

        db.postgis_drop_layer(table)

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
        crs = request.form['srid']

        if not any(ext in f.filename for ext in app.config['SUPPORTED_TYPES']):
            raise IOError("The uploaded file type is not supported")

        elif ".shp" in f.filename:
            raise IOError("A shapefile must be uploaded as a zip with shp, shx, dbf, prj, and cfg files included")

        filename = secure_filename(f.filename)
        layer_name = f.filename.partition('.')[0]

        path = os.path.join(app.config['UPLOAD_DIR'], filename)

        if os.path.exists(path):
            raise IOError("A layer with the same name already exists")

        f.save(path)

        if ".tif" in filename:
            return jsonify({
                'body': True,
                'layer': layer_name,
                'err': None
            })

        else:

            if ".zip" in filename:
                extract_zip(path, app.config['UPLOAD_DIR'], layer_name)
                geom = file.read_vector(os.path.join(app.config['UPLOAD_DIR'], layer_name, f'{layer_name}.shp'))

            else:
                geom = file.read_vector(path)

            geom.set_crs(f'epsg:{crs}', inplace=True, allow_override=True)

            db.postgis_insert(geom, layer_name, crs)
            db.fix_geom_column(layer_name)

            return jsonify({
                'body': True,
                'err': None
            })

    except Exception as e:
        return jsonify({
            'body': None,
            'err': str(e)
        })


@app.route('/download', methods=['POST'])
@cross_origin()
def download():
    req = request.json

    path = os.path.join(app.config['DOWNLOAD_DIR'], req['filename'])
    
    try:
        if ".geojson" in req['filename']:
            response = make_response(send_file(path, mimetype="application/geo+json"))
            response.headers["Content-Type"] = "application/geo+json"
            return response

        elif ".csv" in req['filename']:
            response = make_response(send_file(path, mimetype="text/csv"))
            response.headers["Content-Type"] = "text/csv"
            return response

        else:
            response = make_response(send_file(path, mimetype="application/zip"))
            response.headers["Content-Type"] = "application/zip"
            return response

    except Exception as e:
        return jsonify({
            'err': str(e)
        })


def generate_file(filename, frame=None, alg=None):
    path = os.path.join(app.config['DOWNLOAD_DIR'], filename)

    if ".csv" in filename:
        file.write_csv(frame, path)

    elif "geojson" in filename:
        file.write_vector(frame, path, driver="GeoJSON")

    else:
        name = filename.partition('.')[0]

        raster_files = [
            os.path.join(app.config['DOWNLOAD_DIR'], f'{name}.tif'),
            os.path.join(app.config['DOWNLOAD_DIR'], f'{name}.png')
        ]

        if alg is not None:
            create_zip(raster_files, app.config['DOWNLOAD_DIR'], f'{name}-{alg}.zip')
        else:
            create_zip(raster_files, app.config['DOWNLOAD_DIR'], f'{name}.zip')


# ---------------- ENTRY POINT ----------------
if __name__ == '__main__':
    app.run()
