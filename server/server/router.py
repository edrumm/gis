from server import app
from dotenv import dotenv_values
from flask import jsonify, request
from flask_cors import cross_origin
import psycopg2
from server.database import Database
from server.geometry import *
from server.functions import *

# GDAL
# pip install gdal/GDAL-3.4.1-pp38-pypy38_pp73-win_amd64.whl

try:
   config = dotenv_values('.env')

   pg_user = config.get('PG_USER')
   pg_host = config.get('PG_HOST')
   pg_password = config.get('PG_PASSWORD')
   pg_db = config.get('PG_DB')

   db = Database(pg_host, pg_db, pg_user, pg_password)

   # TODO:
   layers = {}

except (Exception, psycopg2.Error) as err:
   app.logger.error('Could not connect to Postgres: %s', err)
   db = None


@app.route('/', methods=['GET'])
@cross_origin()
def status():
   return jsonify({
      'body': False
   }) if db is None else jsonify({
      'body': True
   })


@app.route('/test', methods=['GET', 'POST'])
@cross_origin()
def test():
   try:
      app.logger.info(count_points_in_polygon(db, 1, 'nyc_subway_stations', 'nyc_polygon'))
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
   return "200 - OK"


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
      result = convex_hull(db, req_body['points'], req_body['table'])

      coords = [(xy[0], xy[1]) for xy in result.exterior.coords]

      # Add to layers

      return jsonify({
         'body': coords,
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
   pass


@app.route('/download', methods=['POST'])
@cross_origin()
def download():
   pass
