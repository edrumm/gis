import os, signal, psycopg2
from flask import Flask

app = Flask(__name__)

import server.database as db


# DB init
try:
   conn, cur = db.connect()

except (Exception, psycopg2.Error) as err:
        print('Error connecting to Postgres:', err)
        exit(1)


@app.route('/')
def hello_world():
   return "Under Construction..."


# Testing ONLY
# Load sample vector dataset from PostGIS
@app.route('/test')
def test():
   cur.execute("""SELECT name, ST_AsText(geom) FROM nyc_subway_stations""")
   points = cur.fetchall()

   return str(points)


if __name__ == '__main__':
   
   # TODO

   app.run()
