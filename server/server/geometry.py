from shapely.geometry import *
from shapely.geometry.base import BaseGeometry


# https://gis.stackexchange.com/questions/114644/adding-a-property-attribute-to-a-geometry-in-shapely-fiona
# http://132.72.155.230:3838/r/vector-layers.html


class Layer:

    def __init__(self, name, srid) -> None:
        self.geometry: BaseGeometry = []
        self.srid = srid
        self.name = name

    # ...


# Convert shapely.BaseGeometry to shapely geometry objects
# is this needed? as just for IDE suggestions

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