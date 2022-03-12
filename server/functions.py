from psycopg2 import sql
import geopandas as gpd
from osgeo import gdal


def count_points_in_polygon(db, polygon, points):

    query = sql.SQL('SELECT gid, geom FROM {polygons}').format(polygons=sql.Identifier(polygon))
    frame = db.postgis(query)

    intersections = []

    frame = frame.reset_index()
    for i, r in frame.iterrows():
        query = sql.SQL('SELECT count(*) FROM {points} WHERE ST_Intersects(geom, (SELECT geom FROM {polygon} WHERE gid = {name}))').format(
            polygon=sql.Identifier(polygon),
            points=sql.Identifier(points),
            name=sql.Literal(r['gid'])
        )

        res = db.postgres_query(query)
        intersections.append(res[0][0])

    frame['intersections'] = intersections

    return frame


def convex_hull(db, table) -> gpd.GeoDataFrame:
    query = sql.SQL('SELECT ST_ConvexHull(ST_Collect(geom)) AS geom FROM {table}').format(
        table=sql.Identifier(table)
    )

    return db.postgis(query)


def voronoi_polygons(db, table) -> gpd.GeoDataFrame:
    query = sql.SQL('SELECT ST_VoronoiPolygons(ST_Collect(geom)) AS geom FROM {table}').format(
        table=sql.Identifier(table)
    )

    return db.postgis(query)


# Raster
def slope():
    pass


def aspect():
    pass


def rasterize():
    pass


def polygonize():
    pass
