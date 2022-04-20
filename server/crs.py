import geopandas as gpd


# Transform a GeoDataFrame to WGS48 projection (EPSG:4326)
def to_WGS84(frame):
    return frame.to_crs("EPSG:4326")
