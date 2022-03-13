from osgeo import gdal
import numpy as np


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


def reclassify(dataset):
    return np.where((dataset >= np.mean(dataset)), 1, 0)


def write_raster(dataset, name, format):
    gt = dataset.GetGeoTransform()
    proj = dataset.GetProjection()

    output = None
    if format == "geotiff":
        output = geotiff.Create(name, xsize=dataset.shape[1], ysize=dataset.shape[0], bands=1, eType=gdal.GDT_Int16)

    else:
        output = bil.Create(name, xsize=dataset.shape[1], ysize=dataset.shape[0], bands=1, eType=gdal.GDT_Int16)

    output.SetProjection(proj)
    output.SetGeoTransform(gt)

    band = output.GetRasterBand(1)
    band.WriteArray(reclassify(dataset))
    band.SetNoValue(np.NaN)
    band.FlushCache()
