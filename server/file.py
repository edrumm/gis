import fiona
import geopandas as gpd


def write_csv(frame, path):
    frame.to_csv(path)


def read_vector(path):
    return gpd.read_file(path)


def write_shapefile(frame, path):
    frame.to_file(path)


def write_geojson(frame, path):
    frame.to_file(path, driver='GeoJSON')
