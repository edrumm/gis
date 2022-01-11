from shapely.geometry import *
from shapely.geometry.base import BaseGeometry


# Convert shapely.BaseGeometry to shapely geometry objects

def to_polygon(geom: BaseGeometry) -> Polygon:
    return geom


def to_multipolygon(geom: BaseGeometry) -> MultiPolygon:
    return geom


def to_point(geom: BaseGeometry) -> Point:
    return geom


def to_multipoint(geom: BaseGeometry) -> MultiPoint:
    return geom


def to_linestring(geom: BaseGeometry) -> LineString:
    return geom


def to_multilinestring(geom: BaseGeometry) -> MultiLineString:
    return geom


def to_geometrycollection(geom: BaseGeometry) -> GeometryCollection:
    return geom