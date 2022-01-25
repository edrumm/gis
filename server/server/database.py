import psycopg2 as pg
from psycopg2 import sql
from shapely import wkb
from shapely.geometry.base import BaseGeometry
from typing import List


class Database:
    def __init__(self, pg_host, pg_db, pg_user, pg_password):
        self.conn = self.connect(pg_host, pg_db, pg_user, pg_password)

    def connect(self, pg_host, pg_db, pg_user, pg_password):
        return pg.connect(host=pg_host, database=pg_db, user=pg_user, password=pg_password)

    def postgis_query(self, sql):
        with self.new_cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()

        return rows

    def new_cursor(self):
        return self.conn.cursor()

    def postgis_insert_new(self, name, srid, geometry: List[BaseGeometry]):
        with self.new_cursor() as cur:
            create_query = sql.SQL('CREATE TABLE IF NOT EXISTS {name} ( id SERIAL PRIMARY KEY, geom geometry NOT NULL )').format(
                name=sql.Identifier(name)
            )    

            cur.execute(create_query)
            self.conn.commit()  

            for geom in geometry:
                query = sql.SQL('INSERT INTO {name} (geom) VALUES ({value})').format(
                    name=sql.Identifier(name),
                    value=sql.Literal(wkb.dumps(geom, hex=True, srid=srid))
                )

                cur.execute(query)
                self.conn.commit()

    def postgis_append(self, name, srid, geom: BaseGeometry):
        with self.new_cursor() as cur:
            query = sql.SQL('INSERT INTO {name} (geom) VALUES ({value})').format(
                name=sql.Identifier(name),
                value=sql.Literal(wkb.dumps(geom, hex=True, srid=srid))
            )

            cur.execute(query)
            self.conn.commit()

    def postgis_drop_layer(self, name):
        with self.new_cursor() as cur:
            query = sql.SQL('DROP TABLE {name}').format(
                name=sql.Identifier(name)
            )

            cur.execute(query)
