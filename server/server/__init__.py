from flask import Flask
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

import server.router

# https://stackoverflow.com/questions/20001229/how-to-get-posted-json-in-flask
# https://stackoverflow.com/questions/13081532/return-json-response-from-flask-view
@app.route('/')
@cross_origin()
def hello_world():
   return "Under Construction..."


if __name__ == '__main__':
   app.run()
