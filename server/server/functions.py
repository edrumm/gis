from server.database import Database
from server.geometry import *
from psycopg2 import sql
from shapely import wkb
from shapely.geometry import Polygon


# Vector
def count_points_in_polygon(db: Database, polygon, table, sub_table) -> int:
    query = sql.SQL('SELECT count(*) FROM {table} WHERE ST_Intersects(geom, (SELECT geom FROM {polygon} WHERE id = {name}))').format(
        table=sql.Identifier(table),
        polygon=sql.Identifier(sub_table),
        name=sql.Literal(polygon)
    )

    try:
        count = db.postgis_query(query)
        return count[0][0]

    except Exception as e:
        # ...
        return e


def convex_hull(db: Database, points, table):
    query = sql.SQL('SELECT ST_ConvexHull(ST_Collect({points})) FROM {table}').format(
        points=sql.Identifier(points),
        table=sql.Identifier(table)
    )

    try:
        result = db.postgis_query(query)
        return { 
            'geom': to_polygon(wkb.loads(result[0][0], hex=True)),
            'id': 0 # TODO - get from db
        }

    except Exception as e:
        # TODO: format e
        return e


# Raster
def slope():
    pass


def viewshed():
    pass
