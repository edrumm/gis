import geopandas as gpd


def to_web_mercator(frame):
    return frame.to_crs(3857)
