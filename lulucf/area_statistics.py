import geopandas as gpd
import numba
import numpy as np

from lulucf.geometry import ops


def areal_percentage_bgt_soilmap(grid, bgt, soilmap, bgt_units, soilmap_units):
    bgt_area = calc_areal_percentage_in_cells(bgt, grid, bgt_units)
    soilmap_area = calc_areal_percentage_in_cells(soilmap, grid, soilmap_units)
    return soilmap_area.values[:, :, :, None] * bgt_area.values[:, :, None, :]


def calc_areal_percentage_in_cells(polygons, lasso_grid, units):
    polygon_area = ops.polygon_area_in_grid(polygons, lasso_grid.dataarray())
    polygon_area.polygon[:] = polygons["idx"].values[polygon_area.polygon]

    cellarea = np.abs(lasso_grid.xsize * lasso_grid.ysize)
    area_grid = lasso_grid.empty_array(units, False)
    area_grid.values = area_to_grid3d(polygon_area, area_grid.values)
    area_grid = area_grid / cellarea
    return area_grid


@numba.njit
def area_to_grid3d(polygon_area, area_grid):
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
