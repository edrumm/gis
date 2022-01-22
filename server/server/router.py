from server import app
from dotenv import dotenv_values
from flask import jsonify, request
from flask_cors import cross_origin
import psycopg2
from typing import List
from server.database import Database
from server.geometry import *
from server.functions import *


# DB init
try:
   config = dotenv_values('.env')

   pg_user = config.get('PG_USER')
   pg_host = config.get('PG_HOST')
   pg_password = config.get('PG_PASSWORD')
   pg_db = config.get('PG_DB')

   db = Database(pg_host, pg_db, pg_user, pg_password)

   layers: List[Layer] = []

except (Exception, psycopg2.Error) as err:
   app.logger.error('Could not connect to Postgres: %s', err)
   db = None


@app.route('/', methods=['GET'])
@cross_origin()
def status():
   return jsonify({
      'connected': False # change to body?
   }) if db is None else jsonify({
      'connected': True
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
   req_body = request.json
   result = count_points_in_polygon(db, layers[req_body['polygon']], req_body['table'], req_body['sub_table'])

   return jsonify({
      'body': result,
      'layer': None # Later ?
   })


@app.route('/convex', methods=['POST'])
@cross_origin()
def convex():
   req_body = request.json
   result = convex_hull(db, req_body['points'], req_body['table'])

   coords = [(xy[0], xy[1]) for xy in result['geom'].exterior.coords]

   app.logger.info(coords)

   layer = Layer('convex_hull_0', 0) # add SRID
   layer.geom_id.append(result['id'])

   layers[layer.name] = layer

   # Returns in JS as [[x, y], [x, y], ...]
   return jsonify({
      'body': coords,
      'layer': {
         'name': layer.name,
         'srid': layer.srid,
         'id': layer.geom_id
      }
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
