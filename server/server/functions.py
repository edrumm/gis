from server.database import Database
from server.geometry import *
from psycopg2 import sql
from shapely import wkb
from shapely.geometry import Polygon


# Vector
def count_points_in_polygon(db: Database, points, polygon, table) -> int:
    query = sql.SQL('SELECT count(*) FROM {table} WHERE ST_Intersects({points}, {polygon})').format(
        table=sql.Identifier(table),
        points=sql.Identifier(points),
        polygon=sql.Identifier(polygon)
    )

    try:
        count = db.postgis_query(query)
        return count[0][0]

    except Exception as e:
        # ...
        return e


def convex_hull(db: Database, points, table) -> Polygon:
    query = sql.SQL('SELECT ST_ConvexHull(ST_Collect({points})) FROM {table}').format(
        points=sql.Identifier(points),
        table=sql.Identifier(table)
    )

    try:
        result = db.postgis_query(query)
        return to_polygon(wkb.loads(result[0][0], hex=True))

    except Exception as e:
        # TODO: format e
        return e


# Raster
def slope():
    pass


def viewshed():
    pass
