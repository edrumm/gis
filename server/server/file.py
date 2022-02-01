import geojson, shapely
from osgeo import gdal, ogr


# https://pcjericks.github.io/py-gdalogr-cookbook/vector_layers.html
def read_shp():
    driver = ogr.GetDriverByName("ESRI Shapefile")
    pass


def write_shp():
    driver = ogr.GetDriverByName("ESRI Shapefile")
    pass


def read_geojson():
    driver = ogr.GetDriverByName("GeoJSON")
    pass


def write_geojson():
    driver = ogr.GetDriverByName("GeoJSON")
    pass


# CSV?


def read_geotiff():
    driver = ogr.GetDriverByName("GTiff")
    pass


def write_geotiff():
    driver = ogr.GetDriverByName("GTiff")
    pass


def read_erdas_img():
    driver = ogr.GetDriverByName("HFA")
    pass


def write_erdas_img():
    driver = ogr.GetDriverByName("HFA")
    pass