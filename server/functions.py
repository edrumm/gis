from psycopg2 import sql
import geopandas as gpd


# VECTOR FUNCTIONS
# Return a GeoDataFrame of count of intersections between 2 tables
def count_points_in_polygon(db, polygon, points):
    query = sql.SQL(' SELECT count(*), b.geom FROM {points} a JOIN {polygons} b ON ST_Intersects(a.geom, b.geom) GROUP BY b.geom').format(
        polygon=sql.Identifier(polygon),
        points=sql.Identifier(points)
    )

    return db.postgis(query)


# Return convex hull geometry
def convex_hull(db, table) -> gpd.GeoDataFrame:
    query = sql.SQL('SELECT ST_ConvexHull(ST_Collect(geom)) AS geom FROM {table}').format(
        table=sql.Identifier(table)
    )

    return db.postgis(query)


# Return Voronoi diagram
def voronoi_polygons(db, table) -> gpd.GeoDataFrame:
    query = sql.SQL('SELECT ST_VoronoiPolygons(ST_Collect(geom)) AS geom FROM {table}').format(
        table=sql.Identifier(table)
    )

    return db.postgis(query)