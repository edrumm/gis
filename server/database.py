import psycopg2 as pg
from psycopg2 import sql
from psycopg2.extensions import register_adapter, AsIs
from sqlalchemy import create_engine
import geopandas as gpd
import numpy


# Config NumPy types, avoids error
# https://stackoverflow.com/questions/50626058/psycopg2-cant-adapt-type-numpy-int64
def addapt_numpy_float64(numpy_float64):
    return AsIs(numpy_float64)


def addapt_numpy_int64(numpy_int64):
    return AsIs(numpy_int64)


# Database class
class Connection:

    def __init__(self, pg_host, pg_db, pg_user, pg_password, pg_port):
        self.conn = pg.connect(host=pg_host, database=pg_db, user=pg_user, password=pg_password)

        # Required for gpd.to_postgis()
        # Convert class to use only sqlalchemy instead of psycopg?
        self.engine = create_engine(f'postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}')

        register_adapter(numpy.float64, addapt_numpy_float64)
        register_adapter(numpy.int64, addapt_numpy_int64)

    def get_conn(self):
        return self.conn

    def close(self):
        self.conn.close()
        self.engine.dispose()

    def table_exists(self, name):
        with self.conn.cursor() as cur:
            query = sql.SQL('SELECT to_regclass(public.{table})').format(table=name)
            cur.execute(query)

            res = cur.fetchall()

        return True if res[0][0] else False

    # Execute a standard PostgreSQL query
    def postgres_query(self, query):
        with self.conn.cursor() as cur:
            cur.execute(query)
            res = cur.fetchall()

        return res

    # Execute a PostGIS query
    def postgis(self, query):
        return gpd.GeoDataFrame.from_postgis(query, self.conn)

    def postgis_insert(self, frame, layer, crs):
        frame.to_postgis(name=layer, con=self.engine)

    def postgis_drop_layer(self, name):
        with self.conn.cursor() as cur:
            query = sql.SQL('DROP TABLE {name}').format(
                name=sql.Identifier(name)
            )

            cur.execute(query)
