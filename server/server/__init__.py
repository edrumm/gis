import psycopg2
from flask import Flask, abort, Response, request

app = Flask(__name__)

import server.database as database
import server.geometry as geom


# DB init
try:
   db = database.Database()
   conn = db.get_conn()

except (Exception, psycopg2.Error) as err:
   app.logger.error('Could not connect to Postgres: %s', err)
   abort(Response(str(err)))


@app.route('/')
def hello_world():
   return "Under Construction..."


# Testing ONLY
# Load sample vector dataset from PostGIS
@app.route('/test')
def test():
   points = db.postgis_query("""SELECT name, ST_AsText(geom) FROM nyc_subway_stations""")
   app.logger.info(points)

   return str(points)


if __name__ == '__main__':
   
   # TODO

   app.run()
