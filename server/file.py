import geopandas as gpd


# VECTOR FILE HANDLING

def write_csv(frame, path):
    frame.to_csv(path)


def read_vector(path):
    return gpd.read_file(path)


def write_vector(frame, path, driver=None):
    if driver is not None:
        frame.to_file(path, driver=driver)
    else:
        frame.to_file(path)


def write_csv(frame, path):
    frame.to_csv(path, na_rep="NULL")
