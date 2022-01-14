import psycopg2 as pg


class Database:
    def __init__(self, pg_host, pg_db, pg_user, pg_password):
        self.conn = self.connect(pg_host, pg_db, pg_user, pg_password)

    def connect(self, pg_host, pg_db, pg_user, pg_password):
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