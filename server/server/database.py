import psycopg2 as pg
from psycopg2 import sql
from server.geometry import Layer
from shapely import wkb


class Database:
    def __init__(self, pg_host, pg_db, pg_user, pg_password):
        self.conn = self.connect(pg_host, pg_db, pg_user, pg_password)

    def connect(self, pg_host, pg_db, pg_user, pg_password):
        conn = pg.connect(host=pg_host, database=pg_db, user=pg_user, password=pg_password)

        return conn

    def postgis_query(self, sql):
        with self.new_cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()

        return rows

    def get_conn(self):
        return self.conn

    def new_cursor(self):
        return self.conn.cursor()

    # Needs test
    def postgis_insert_new(self, layer: Layer):
        with self.new_cursor() as cur:
            create_query = sql.SQL('CREATE TABLE IF NOT EXISTS {name} ( id SERIAL PRIMARY KEY, geom geometry NOT NULL )').format(
                name=sql.Identifier(layer.name)
            )    

            cur.execute(create_query)
            self.conn.commit()  

            for geom in layer.geometry:
                query = sql.SQL('INSERT INTO {name}(geom) VALUES ({wkb_value})').format(
                    name=sql.Identifier(layer.name),
                    wkb_value=sql.Identifier(wkb.dumps(geom, hex=True, srid=layer.srid))
                )

                cur.execute(query)
                self.conn.commit()  

    def postgis_insert(self, table):
        pass