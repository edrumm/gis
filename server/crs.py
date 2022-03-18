import geopandas as gpd


def change_crs(frame: gpd.GeoDataFrame, code):
    return frame.to_crs(crs=code)