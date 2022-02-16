from typing import List
import geojson, shapefile
from PIL import Image
from shapely.geometry import shape
from shapely.geometry.base import BaseGeometry

# Neither working
# from osgeo import gdal, ogr
# import fiona


# https://pcjericks.github.io/py-gdalogr-cookbook/vector_layers.html
def read_shp(file):
    r = shapefile.Reader(file)
    return r.shapes()


def write_shp():
    pass


def read_geojson(file) -> List[BaseGeometry]:
    geom = geojson.loads(file.read())

    file.close()

    return [shape(feature['geometries']) for feature in geom['features']]


def write_geojson():
    pass


def csv():
    pass


def read_geotiff():
    pass


def write_geotiff():
    pass


def read_img():
    pass


def write_img():
    pass