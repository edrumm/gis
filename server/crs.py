import geopandas as gpd


# Transform a GeoDataFrame to Web Mercator projection (EPSG:3857)
def to_web_mercator(frame):
    return frame.to_crs(crs="EPSG:3857")
