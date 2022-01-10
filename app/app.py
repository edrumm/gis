import os, signal
import database
import user.auth as auth
from flask import Flask

app = Flask(__name__)
# app.register_blueprint(postgres)


@app.route('/')
def hello_world():
   return auth.test()


def stop():
   pass


if __name__ == '__main__':
   signal.signal(signal.SIGTERM, stop)
   signal.signal(signal.SIGINT, stop)
   signal.signal(signal.SIGKILL, stop)

   # Read env
   # print(os.environ.get('PG_HOST'))
   conn, cur = database.connect()

   app.run()