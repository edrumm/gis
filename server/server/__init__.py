import signal
from flask import Flask

app = Flask(__name__)

import server.database as db


@app.route('/')
def hello_world():
   return db.test()


def stop():
   pass


if __name__ == '__main__':
   signal.signal(signal.SIGTERM, stop)
   signal.signal(signal.SIGINT, stop)
   signal.signal(signal.SIGKILL, stop)

   # Read env
   # conn, cur = db.connect()

   app.run()