from typing import List, TypeVar

import geopandas as gpd
import numba
import numpy as np
import xarray as xr

from lulucf.geometry import ops

LassoGrid = TypeVar("LassoGrid")


def areal_percentage_bgt_soilmap(
    grid: LassoGrid,
    bgt: gpd.GeoDataFrame,
    soilmap: gpd.GeoDataFrame,
    bgt_units: List[str],
    soilmap_units: List[str],
) -> np.ndarray:
    """
    Calculate per cell in a grid for each combination of BGT and Soil Map polygons what
    percentage of a cell is covered by the combination. This returns a 3D output array
    with dimensions ('y', 'x', 'layer') where the dimension 'layer' (axis=2) contains
    ordered BGT-Soilmap layer combinations.

    Parameters
    ----------
    grid : lulucf.LassoGrid
        LassoGrid instance containing the raster grid to calculate the percentages for.
    bgt : gpd.GeoDataFrame
        GeoDataFrame containing the BGT data polygons.
    soilmap : gpd.GeoDataFrame
        GeoDataFrame containing the BGT data polygons.
    bgt_units : List[str]
        List containing the ordered unique BGT layers. This determines the ordering of the
        BGT-Soilmap combinations in the output DataArray.
    soilmap_units : List[str]
        List containing the ordered unique Soilmap layers. This determines the ordering of
        the BGT-Soilmap combinations in the output DataArray.

    Returns
    -------
    np.ndarray
        3D array with the areal percentages.

    """
    bgt_area = calc_areal_percentage_in_cells(bgt, grid, bgt_units)
    soilmap_area = calc_areal_percentage_in_cells(soilmap, grid, soilmap_units)
    return soilmap_area.values[:, :, :, None] * bgt_area.values[:, :, None, :]


def calc_areal_percentage_in_cells(
    polygons: gpd.GeoDataFrame, lasso_grid: LassoGrid, units: List[str]
) -> xr.DataArray:
    """
    Calculate in each grid cell the proportion of the area that is covered by each polygon
    in a GeoDataFrame.

    Parameters
    ----------
    polygons : gpd.GeoDataFrame
        _description_
    lasso_grid : LassoGrid
        _description_
    units : List[str]
        _description_

    Returns
    -------
    xr.DataArray
        _description_
    """
    # Needs unique polygons, otherwise area calculation goes wrong
    polygons = polygons.explode()
    polygon_area = ops.polygon_area_in_grid(polygons, lasso_grid.dataarray())
    polygon_area.polygon[:] = polygons["idx"].values[polygon_area.polygon]

    cellarea = np.abs(lasso_grid.xsize * lasso_grid.ysize)
    area_grid = lasso_grid.empty_array(units, False)
    area_grid.values = area_to_grid3d(polygon_area, area_grid.values)
    area_grid = area_grid / cellarea
    return area_grid


def calculate_model_flux(model: gpd.GeoDataFrame, grid: LassoGrid) -> xr.DataArray:
    """
    Calculate a weighted flux per cell in a 2D grid from Somers emissions data.

    Parameters
    ----------
    somers : gpd.GeoDataFrame
        GeoDataFrame containing Somers emissions per polygon.
    grid : LassoGrid
        2D grid to calculate the emission fluxes for.

    Returns
    -------
    xr.DataArray
        2D grid with weighted emission flux per cell.

    """
    flux_grid = grid.dataarray(np.nan)
    model = model.explode()
    area = ops.polygon_area_in_grid(model, flux_grid)
    flux = model["flux_m2"].values[area.polygon]

    flux_grid.values = flux_to_grid(flux, area, flux_grid.values)
    return flux_grid


@numba.njit
def area_to_grid3d(
    polygon_area: ops.PolygonGridArea, area_grid: np.ndarray
) -> np.ndarray:
    """
    Translate calculated areas for polygons per grid cell into a 3D grid.

    Parameters
    ----------
    polygon_area : ops.PolygonGridArea
        _description_
    area_grid : np.ndarray
        _description_

    Returns
    -------
    np.ndarray
        _description_
    """
    _, nx, nz = area_grid.shape

    min_idx = 0
    for i in range(len(polygon_area.cell_idx)):
        cell_idx = polygon_area.cell_idx[i]
        nitems = polygon_area.cell_indices[i]
        max_idx = min_idx + nitems

        polygons = polygon_area.polygon[min_idx:max_idx]
        area = polygon_area.area[min_idx:max_idx]

        area = np.bincount(polygons, weights=area, minlength=nz)
        row, col = np.divmod(cell_idx, nx)

        area_grid[row, col, :] = area
        min_idx += nitems

    return area_grid


# @numba.njit
def flux_to_grid(
    flux: np.ndarray, area: ops.PolygonGridArea, grid: np.ndarray
) -> np.ndarray:
    """
    Translate Somers emissions for polygons to a 2D grid containing a weighted flux by
    area based on the calculated area of each polygon in a cell.

    Parameters
    ----------
    flux : np.ndarray
        _description_
    area : ops.PolygonGridArea
        _description_
    grid : np.ndarray
        _description_

    Returns
    -------
    np.ndarray
        _description_
    """
    _, nx = grid.shape
    min_idx = 0
    for i in range(len(area.cell_idx)):
        cell_idx = area.cell_idx[i]
        nitems = area.cell_indices[i]
        max_idx = min_idx + nitems

        f = flux[min_idx:max_idx]
        a = area.area[min_idx:max_idx]

        row, col = np.divmod(cell_idx, nx)
        grid[row, col] = _weighted_average(f, a)
        min_idx += nitems

    return grid


# @numba.njit
def _weighted_average(flux: np.ndarray, area: np.ndarray) -> np.ndarray:
    """
    Helper function for weighted average in Numba compiled functions.

    """
    return np.sum(flux * area) / np.sum(area)
