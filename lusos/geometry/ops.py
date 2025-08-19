from typing import NamedTuple

import geopandas as gpd
import mapbox_earcut as earcut
import numpy as np
import shapely
import xarray as xr
import xugrid as xu


class PolygonGridArea(NamedTuple):
    """
    Sparse matrix-like structure for the result of `polygon_area_in_grid` containing the
    indices of the grid cells that overlap with polygons, the number of polygons that
    overlap with those grid cells, the index ids of the polygons and the corresponding
    area in the grid cell.

    Parameters
    ----------
    cell_idx : np.ndarray
        Indices of the grid cells that overlap with polygons.
    nitems : np.ndarray
        Number of polygons that overlap with the grid cell.
    polygon : np.ndarray
        Index id of the polygon that overlaps with the grid cell.
    area : np.ndarray
        Area of the polygon in the grid cell.
    """

    cell_idx: np.ndarray
    nitems: np.ndarray
    polygon: np.ndarray
    area: np.ndarray


class Triangles(NamedTuple):
    triangles: np.ndarray
    index: np.ndarray
    coords: np.ndarray


def triangulate(polygons: gpd.GeoDataFrame) -> Triangles:
    triangles = []
    index = []
    coords = []

    increment = 0
    for ii, polygon in enumerate(polygons["geometry"]):
        vertices = shapely.get_coordinates(polygon)
        n_vertices = len(vertices)
        interior_verts = shapely.get_num_coordinates(polygon.interiors)

        if interior_verts.any():
            end_of_exterior = n_vertices - np.sum(interior_verts)
            vert_indices = np.append(
                end_of_exterior, np.cumsum(interior_verts) + end_of_exterior
            )
        else:
            vert_indices = [n_vertices]

        connectivity = earcut.triangulate_float64(vertices, vert_indices)

        triangles.append(connectivity + increment)
        coords.append(vertices)
        index.append(np.full(len(connectivity) // 3, ii))
        increment += len(vertices)

    triangles = np.concatenate(triangles).reshape((-1, 3))
    index = np.concatenate(index)
    coords = np.concatenate(coords)
    return Triangles(triangles, index, coords)


def polygon_area_in_grid(
    polygons: gpd.GeoDataFrame, grid: xr.DataArray
) -> PolygonGridArea:
    tri = triangulate(polygons)

    ugrid = xu.Ugrid2d(*tri.coords.T, -1, tri.triangles)
    regridder = xu.OverlapRegridder(source=ugrid, target=grid)
    ds = regridder.to_dataset()

    cell_idx_pointer = ds["__regrid_indptr"].to_numpy()
    polygon_idx = ds["__regrid_indices"].to_numpy()
    area = ds["__regrid_data"].to_numpy()

    nonzero_per_row = np.diff(cell_idx_pointer)
    cell_idx = np.flatnonzero(nonzero_per_row)
    nitems = nonzero_per_row[cell_idx]

    return PolygonGridArea(cell_idx, nitems, tri.index[polygon_idx], area)


def triangles_to_geodataframe(triangles: Triangles) -> gpd.GeoDataFrame:
    return gpd.GeoDataFrame(
        geometry=shapely.polygons(triangles.coords[triangles.triangles]), crs=28992
    )
