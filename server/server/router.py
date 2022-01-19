from server import app
from dotenv import dotenv_values
from flask import abort, Response, jsonify, request
from flask_cors import cross_origin
import psycopg2
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
   conn = db.get_conn()

except (Exception, psycopg2.Error) as err:
   app.logger.error('Could not connect to Postgres: %s', err)
   abort(Response(str(err)))


# Testing ONLY
# Load sample vector dataset from PostGIS
#
# const data = {
#   points: 'geom',
#   table: 'nyc_subway_stations'
# };
#
# const options = {
#   method: 'POST',
#   headers: {
#     'Content-Type': 'application/json'
#   },
#   body: JSON.stringify(data)
# };
#
# fetch('/test', options)
# .then(res => res.json())
# .then(json => console.log(json.body))
# .catch(err => console.error(err));
#
@app.route('/test', methods=['GET', 'POST'])
@cross_origin()
def test():
   req_body = request.json
   points = convex_hull(db, req_body['points'], req_body['table'])
   app.logger.info(points)

   return jsonify({
      'body': str(points)
   })


@app.route('/count', methods=['POST'])
@cross_origin()
def count():
   pass


@app.route('/convex', methods=['POST'])
@cross_origin()
def convex():
   pass


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
