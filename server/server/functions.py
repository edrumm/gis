from server.database import Database
from psycopg2 import sql
from shapely import wkb # maybe
from osgeo import gdal
import geojson


# Vector
def count_points_in_polygon(db: Database, polygon, points, sub_table) -> int:
    query = sql.SQL('SELECT count(*) FROM {points} WHERE ST_Intersects(geom, (SELECT geom FROM {polygon} WHERE id = {name}))').format(
        points=sql.Identifier(points),
        polygon=sql.Identifier(sub_table),
        name=sql.Literal(polygon)
    )

    count = db.postgis_query(query)
    return count[0][0]


def convex_hull(db: Database, points, table):
    query = sql.SQL('SELECT ST_AsGeoJson(ST_ConvexHull(ST_Collect({points}))) FROM {table}').format(
        points=sql.Identifier(points),
        table=sql.Identifier(table)
    )

    result = db.postgis_query(query)
    return geojson.loads(result[0][0])


# Raster
def slope():
    pass


def viewshed():
    pass
