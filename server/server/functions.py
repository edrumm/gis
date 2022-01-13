import server.database as database
import server.geometry as geom
from psycopg2 import sql
from shapely import wkb


def count_points_in_polygon(db: database, points, polygon, table):
    pass


def convex_hull(db: database.Database, points, table):
    query = sql.SQL('SELECT ST_ConvexHull(ST_Collect({points})) FROM {table}').format(
        points=sql.Identifier(points),
        table=sql.Identifier(table)
    )

    try:
        result = db.postgis_query(query)
        return geom.to_polygon(wkb.loads(result[0][0], hex=True))

    except Exception as e:
        # TODO: format e
        return e


def slope():
    pass


def viewshed():
    pass