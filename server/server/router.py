from server import app
from dotenv import dotenv_values
from flask import jsonify, request, session
from flask_cors import cross_origin
from werkzeug.utils import secure_filename
from shapely.geometry import shape
import psycopg2
import os

from server.database import Database
from server.file import *
from server.functions import *


try:
   config = dotenv_values('.env')

   pg_user = config.get('PG_USER')
   pg_host = config.get('PG_HOST')
   pg_password = config.get('PG_PASSWORD')
   pg_db = config.get('PG_DB')

   db = Database(pg_host, pg_db, pg_user, pg_password)

except (Exception, psycopg2.Error) as err:
   app.logger.error('Could not connect to Postgres: %s', err)
   db = None


ALLOWED_EXTENSIONS = set(['shp', 'shx', 'dbf', 'prj', 'zip', 'tiff', 'tif', 'geojson', 'img'])


@app.route('/', methods=['GET'])
@cross_origin()
def status():
   return jsonify({
      'body': False
   }) if db is None else jsonify({
      'body': True
   })


# Test route only, not to be used in production
@app.route('/test', methods=['GET', 'POST'])
@cross_origin()
def test():
   try:
      geom = convex_hull(db, 'geom', 'nyc_subway_stations')
      return jsonify(geom)
   except Exception as e:
      return str(e)

   """
   req_body = request.json
   points = convex_hull(db, req_body['points'], req_body['table'])
   app.logger.info(points)

   return jsonify({
      'body': str(points)
   })
   """


@app.route('/count', methods=['POST'])
@cross_origin()
def count():
   try:
      req_body = request.json
      result = count_points_in_polygon(db, req_body['polygon'], req_body['points'], req_body['sub_table'])

      return jsonify({
         'body': result,
         'layer': None,
         'err': None
      })

   except Exception as e:
      return jsonify({
         'body': None,
         'layer': None,
         'err': str(e)
      })


@app.route('/convex', methods=['POST'])
@cross_origin()
def convex():
   try:
      req_body = request.json
      geom = convex_hull(db, req_body['table'])

      return jsonify({
         'body': geom,
         'layer': None,
         'err': None
      })

   except Exception as e:
      return jsonify({
         'body': None,
         'layer': None,
         'err': str(e)
      })


@app.route('/voronoi', methods=['POST'])
@cross_origin()
def voronoi_polygon():
   try:
      req_body = request.json
      geom = voronoi(db, req_body['table'])

      return jsonify({
         'body': geom,
         'layer': None,
         'err': None
      })

   except Exception as e:
      return jsonify({
         'body': None,
         'layer': None,
         'err': str(e)
      })


@app.route('/slope', methods=['POST'])
@cross_origin()
def slope():
   pass


@app.route('/viewshed', methods=['POST'])
@cross_origin()
def viewshed():
   pass


@app.route('/upload', methods=['POST'])
@cross_origin()
def upload():
   try:

      if not os.path.isdir(app.config['UPLOAD_DIR']):
         os.mkdir(app.config['UPLOAD_DIR'])

      file = request.files['file']

      geom = read_geojson(file)

      layer_name = file.filename.partition('.')[0]

      # db.postgis_insert_new(layer_name, 26918, geom)

      # filename = secure_filename(file.filename)

      # file.save(os.path.join(app.config['UPLOAD_DIR'], filename))

      # session['uploadFilePath'] = destination

   except Exception as e:
      app.logger.error(e)

      return jsonify({
         'body': None,
         'err': str(e)
      })

   """
   if '.shp' in file.filename:
      read_shp() # ...

   elif '.geojson' in file.filename:
      read_geojson()

   elif '.tiff' in file.filename or '.tif' in file.filename:
      read_geotiff()

   elif '.img' file.filename:
      read_img()

   else:
      return jsonify({
         'body': None,
         'err': 'Invalid or unsupported file format'
      })
   """

   return jsonify({
      'body': geom,
      'layer': layer_name,
      'err': None
   })


@app.route('/download', methods=['POST'])
@cross_origin()
def download():
   pass
