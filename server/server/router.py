from server import app
from dotenv import dotenv_values
from flask import abort, Response, jsonify #, request (maybe required later)
from flask_cors import cross_origin
import psycopg2
import server.database as database
from server.geometry import *
from server.functions import *


# DB init
try:
   config = dotenv_values('.env')

   pg_user = config.get('PG_USER')
   pg_host = config.get('PG_HOST')
   pg_password = config.get('PG_PASSWORD')
   pg_db = config.get('PG_DB')

   db = database.Database(pg_host, pg_db, pg_user, pg_password)
   conn = db.get_conn()

except (Exception, psycopg2.Error) as err:
   app.logger.error('Could not connect to Postgres: %s', err)
   abort(Response(str(err)))


# Testing ONLY
# Load sample vector dataset from PostGIS
@app.route('/test')
@cross_origin()
def test():
   points = convex_hull(db, 'geom', 'nyc_subway_stations')
   app.logger.info(points)

   return str(points)


@app.route('/count')
@cross_origin()
def count():
   pass


@app.route('/convex')
@cross_origin()
def convex():
   pass


@app.route('/slope')
@cross_origin()
def slope():
   pass


@app.route('/viewshed')
@cross_origin()
def viewshed():
   pass


@app.route('/upload')
@cross_origin()
def upload():
   pass


@app.route('/download')
@cross_origin()
def download():
   pass
