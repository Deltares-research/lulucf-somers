import geopandas as gpd
import numpy as np
import pandas as pd
import xarray as xr
from shapely.geometry import Polygon

from lulucf.utils import _add_layer_idx_column, cell_as_geometry


def calculate_areal_percentages_bgt(bgt_data: gpd.GeoDataFrame, da: xr.DataArray):
    bgt_data = _add_layer_idx_column(bgt_data, da)
    da = calc_areal_percentage_in_cells(bgt_data, da)
    return da


def calculate_areal_percentages_soilmap(soilmap: gpd.GeoDataFrame, da: xr.DataArray):
    soilmap = _add_layer_idx_column(soilmap, da)
    da = calc_areal_percentage_in_cells(soilmap, da)
    return da


def _calc_percentage(
    cell: Polygon, gdf: gpd.GeoDataFrame, area: int | float, ntypes: int
):
    """
    Helper function to calculate the areal percentages of each polygon in a cell geometry.

    """
    cell_clip = gdf.clip(cell)
    percentage = cell_clip["geometry"].area.values / area
    idx = cell_clip["idx"].values
    percentage = np.bincount(idx, weights=percentage, minlength=ntypes)
    return percentage


def calc_areal_percentage_in_cells(polygons: gpd.GeoDataFrame, da: xr.DataArray):
    if "idx" not in polygons.columns:
        raise KeyError("GeoDataFrame must contain an 'idx' column.")

    if "y" not in da.dims or "x" not in da.dims:
        raise KeyError("DataArray must contain dimensions 'y' and 'x'.")

    cellsize = da.rio.resolution()
    cellarea = np.abs((cellsize[0] * cellsize[1]))
    nlayers = len(da["layer"])

    for i, y in enumerate(da["y"]):
        for j, x in enumerate(da["x"]):
            geom = cell_as_geometry(x, y, cellsize)
            percentage = _calc_percentage(geom, polygons, cellarea, nlayers)
            da[i, j] = percentage

    return da


def calc_areal_percentages_for(
    indices: np.ndarray,
    bgt_data: gpd.GeoDataFrame,
    soilmap: gpd.GeoDataFrame,
    bgt_da: xr.DataArray,
    soilmap_da: xr.DataArray,
):
    cellsize = bgt_da.rio.resolution()
    cellarea = np.abs(cellsize[0] * cellsize[1])

    n_bgt_layers = len(bgt_da["layer"])
    n_soilmap_layers = len(soilmap_da["layer"])

    for idx in indices:
        i, j = idx[0], idx[1]
        y, x = bgt_da["y"][i], bgt_da["x"][j]
        geom = cell_as_geometry(x, y, cellsize)

        perc = _calc_percentage(geom, bgt_data, cellarea, n_bgt_layers)
        bgt_da[i, j] = perc

        perc = _calc_percentage(geom, soilmap, cellarea, n_soilmap_layers)
        soilmap_da[i, j] = perc

    return bgt_da, soilmap_da
