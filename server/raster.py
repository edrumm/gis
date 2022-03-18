from osgeo import gdal
import matplotlib.pyplot as plt
import numpy as np


# Register GDAL drivers for GeoTiff and BIL
# (May not be required for DEMProcessing)
geotiff = gdal.GetDriverByName("GTiff")
bil = gdal.GetDriverByName("EHdr")

geotiff.Register()
bil.Register()


def slope(dataset, output):
    slope_data = gdal.DEMProcessing(output, dataset, "slope", computeEdges=True)

    return slope_data.GetRasterBand(1).ReadAsArray()


def aspect(dataset, output):
    asp_data = gdal.DEMProcessing(output, dataset, "aspect", computeEdges=True)

    return asp_data.GetRasterBand(1).ReadAsArray()


def rasterize():
    pass


def polygonize():
    pass


def get_gdal_dataset(file):
    return gdal.Open(file)


def write_raster(dataset, path):
    figure = plt.figure()

    plt.imshow(np.where((dataset >= np.mean(dataset)), 1, 0), cmap='tab20_r')
    plt.gca().set_axis_off()
    plt.subplots_adjust(top=1, bottom=0, left=0, right=1, hspace=0, wspace=0)
    plt.margins(0, 0)

    figure.savefig(path, dpi=figure.dpi, bbox_inches='tight', pad_inches=0, transparent=True)
