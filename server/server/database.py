import psycopg2 as pg
from dotenv import dotenv_values

class Database:
    def __init__(self):
        self.conn = self.connect()

    def connect(self):
        config = dotenv_values('.env')

        pg_user = config.get('PG_USER')
        pg_host = config.get('PG_HOST')
        pg_password = config.get('PG_PASSWORD')
        pg_db = config.get('PG_DB')

        conn = pg.connect(host=pg_host, database=pg_db, user=pg_user, password=pg_password)

        return conn

    def postgis_query(self, sql):
        with self.conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()

        return rows

    def get_conn(self):
        return self.conn

    def new_cursor(self):
        return self.conn.cursor()