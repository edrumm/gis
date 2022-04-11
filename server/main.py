from flask import Flask, jsonify, request, send_file
from flask_cors import CORS, cross_origin
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


# TODO Remove
def generate_file_num():
    num = 0

    while True:
        yield num
        num += 1


file_num = generate_file_num()

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

        tif_path = os.path.join(app.config['DOWNLOAD_DIR'], f'{filename}.tif')
        png_path = os.path.join(app.config['DOWNLOAD_DIR'], f'{filename}.png')

        slp = raster.aspect(ds, tif_path)
        raster.write_raster(slp, png_path)

        # create_zip([tif_path, png_path], app.config['DOWNLOAD_DIR'], f'{filename}-slope.zip')
        download(f'{filename}.tif')

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

        tif_path = os.path.join(app.config['DOWNLOAD_DIR'], f'{filename}.tif')
        png_path = os.path.join(app.config['DOWNLOAD_DIR'], f'{filename}.png')

        asp = raster.aspect(ds, tif_path)
        raster.write_raster(asp, png_path)

        # create_zip([tif_path, png_path], app.config['DOWNLOAD_DIR'], f'{filename}-aspect.zip')
        download(f'{filename}.tif')

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
        """
        geom: gpd.GeoDataFrame = file.read_vector("C:\\Users\\esd06\\Documents\\4TH-YEAR\\Honours-Project\\sample data\\nyc\\nyc_subway_stations.geojson")
        geom.set_crs(epsg=26918, inplace=True, allow_override=True)
        
        """

        extract_zip("C:\\Users\\esd06\\Documents\\4TH-YEAR\\Honours-Project\\sample data\\nyc\\nyc_subway_stations.zip",
                    app.config['UPLOAD_DIR'], "nyc_subway_stations")

        geom = file.read_vector(os.path.join(app.config['UPLOAD_DIR'], "nyc_subway_stations", "nyc_subway_stations.shp"))

        download("nyc_subway_stations.geojson", geom)
        download("nyc_subway_stations.csv", geom)
        download("nyc_subway_stations.shp", geom)

        return jsonify({
            'body': geom.to_json(),
            'crs': str(geom.crs),
            'layer': None,
            'err': None
        })

    except Exception as err:
        return jsonify({
            'body': None,
            'layer': None,
            'err': str(err)
        })


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

        if db.table_exists(layer_name):
            raise IOError("A layer with the same name already exists")

        path = os.path.join(app.config['UPLOAD_DIR'], filename)
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
                geom = file.read_vector(os.path.join(path, layer_name, f'{layer_name}.shp'))

            else:
                geom = file.read_vector(path)

            # TODO: Get CRS value from request
            # geom.set_crs(epsg=26918, inplace=True, allow_override=True)

            db.postgis_insert(geom, layer_name, 26918)

            geom = crs.to_web_mercator(geom)
            os.remove(path)

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


def download(filename, frame=None):
    path = os.path.join(app.config['DOWNLOAD_DIR'], filename)

    if ".csv" in filename:
        file.write_csv(frame, path)

    elif ".shp" in filename:
        file.write_vector(frame, path)
        name = filename.partition('.')[0]

        shp_aux_files = [
            os.path.join(app.config['DOWNLOAD_DIR'], f'{name}.shp'),
            os.path.join(app.config['DOWNLOAD_DIR'], f'{name}.shx'),
            os.path.join(app.config['DOWNLOAD_DIR'], f'{name}.dbf'),
            os.path.join(app.config['DOWNLOAD_DIR'], f'{name}.prj'),
            os.path.join(app.config['DOWNLOAD_DIR'], f'{name}.cpg')
        ]

        create_zip(shp_aux_files, app.config['DOWNLOAD_DIR'], f'{name}.zip')

        for f in shp_aux_files:
            os.remove(f)

    elif "geojson" in filename:
        file.write_vector(frame, path, driver="GeoJSON")

    else:
        name = filename.partition('.')[0]

        raster_files = [
            os.path.join(app.config['DOWNLOAD_DIR'], f'{name}.tif'),
            os.path.join(app.config['DOWNLOAD_DIR'], f'{name}.png')
        ]

        create_zip(raster_files, app.config['DOWNLOAD_DIR'], f'{name}.zip')


# ---------------- ENTRY POINT ----------------
if __name__ == '__main__':
    app.run()
