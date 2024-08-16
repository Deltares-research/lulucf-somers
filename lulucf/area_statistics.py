import geopandas as gpd
import xarray as xr

from lulucf.utils import cell_as_geometry


def calc_areal_percentage_in_cells(bgt_data: gpd.GeoDataFrame, da: xr.DataArray):
    cellsize = da.rio.resolution()
    for i, y in da['y']:
        for j, x in da['x']:
            geom = cell_as_geometry(x, y, cellsize)
    return
