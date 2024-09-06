import geopandas as gpd
import numpy as np
import pandas as pd
import xarray as xr
from shapely.geometry import Polygon

from lulucf.utils import _add_layer_idx_column, cell_as_geometry


def somers_flux_in(cell: Polygon, somers: gpd.GeoDataFrame):
    cell_clip = somers.clip(cell)
    flux = np.average(cell_clip["median"], weights=cell_clip["geometry"].area)
    return flux


def calc_flux_and_coverage_for(
    indices: np.ndarray,
    somers: gpd.GeoDataFrame,
    bgt_data: gpd.GeoDataFrame,
    soilmap: gpd.GeoDataFrame,
    flux: xr.DataArray,
    areal_da: xr.DataArray,
):
    cellsize = flux.rio.resolution()
    cellarea = np.abs(cellsize[0] * cellsize[1])

    n_bgt_layers = bgt_data["layer"].nunique()
    n_soilmap_layers = soilmap["layer"].nunique()

    for idx in indices:
        i, j = idx[0], idx[1]
        y, x = flux["y"][i], flux["x"][j]
        geom = cell_as_geometry(x, y, cellsize)

        flux[i, j] = somers_flux_in(geom, somers)

        bgt_perc = _calc_coverage_percentage(geom, bgt_data, cellarea, n_bgt_layers)
        soilmap_perc = _calc_coverage_percentage(
            geom, soilmap, cellarea, n_soilmap_layers
        )

        areal_da[i, j] = np.outer(soilmap_perc, bgt_perc).ravel()

    return flux, areal_da


def _calc_coverage_percentage(
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


def calculate_areal_percentages_bgt(bgt_data: gpd.GeoDataFrame, da: xr.DataArray):
    bgt_data = _add_layer_idx_column(bgt_data, da)
    da = calc_areal_percentage_in_cells(bgt_data, da)
    return da


def calculate_areal_percentages_soilmap(soilmap: gpd.GeoDataFrame, da: xr.DataArray):
    soilmap = _add_layer_idx_column(soilmap, da)
    da = calc_areal_percentage_in_cells(soilmap, da)
    return da


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
            percentage = _calc_coverage_percentage(geom, polygons, cellarea, nlayers)
            da[i, j] = percentage

    return da
