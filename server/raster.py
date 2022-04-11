from osgeo import gdal
import matplotlib.pyplot as plt
import numpy as np


# Register GDAL GeoTIFF driver
geotiff = gdal.GetDriverByName("GTiff")
geotiff.Register()


# RASTER FUNCTIONS
# Perform slope computation and return as NumPy array
def slope(dataset, output):
    slope_data = gdal.DEMProcessing(output, dataset, "slope", computeEdges=True, slopeFormat="percent")

    return slope_data.GetRasterBand(1).ReadAsArray()


# Perform aspect computation and return as NumPy array
def aspect(dataset, output):
    asp_data = gdal.DEMProcessing(output, dataset, "aspect", computeEdges=True, zeroForFlat=True)

    return asp_data.GetRasterBand(1).ReadAsArray()


# Open file as a GDAL dataset
def get_gdal_dataset(file):
    return gdal.Open(file)


# Plot and colour raster as a PNG image
def write_raster(dataset, path):
    figure = plt.figure()

    plt.imshow(dataset, cmap='jet')
    plt.gca().set_axis_off()
    plt.subplots_adjust(top=1, bottom=0, left=0, right=1, hspace=0, wspace=0)
    plt.margins(0, 0)

    figure.savefig(path, dpi=figure.dpi, bbox_inches='tight', pad_inches=0, transparent=True)
