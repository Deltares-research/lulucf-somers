import geopandas as gpd
import mapbox_earcut as earcut
import numpy as np
import pandas as pd
import shapely
import xarray as xr
import xugrid as xu


def polygon_coords(polygons: gpd.GeoDataFrame):
    coords, index = shapely.get_coordinates(
        polygons["geometry"].exterior.to_numpy(), return_index=True
    )
    return coords, index


def triangulate(coords: np.ndarray, index: np.ndarray):
    polygon_split_indices = np.flatnonzero(np.diff(index)) + 1
    vertices = np.split(coords, polygon_split_indices)

    triangles = []
    index = []

    increment = 0
    for ii, verts in enumerate(vertices):
        connectivity = earcut.triangulate_float64(verts, [len(verts)])
        triangles.append(connectivity + increment)
        index.append(np.full(len(connectivity) // 3, ii))
        increment += len(verts)

    triangles = np.concatenate(triangles).reshape((-1, 3))
    index = np.concatenate(index)
    return triangles, index


def polygon_area_in_grid(polygons: gpd.GeoDataFrame, grid: xr.DataArray):
    coords, index = polygon_coords(polygons)
    triangles, index = triangulate(coords, index)

    ugrid = xu.Ugrid2d(*coords.T, -1, triangles)
    regridder = xu.OverlapRegridder(source=ugrid, target=grid)
    ds = regridder.to_dataset()

    cell_idx_pointer = ds["__regrid_indptr"].to_numpy()
    polygon_idx = ds["__regrid_indices"].to_numpy()
    area = ds["__regrid_data"].to_numpy()
    nrows = ds["__regrid_n"]

    nonzero_per_row = np.diff(cell_idx_pointer)
    cell_idx = np.repeat(np.arange(nrows), nonzero_per_row)

    return pd.DataFrame(  # TODO: Don't use DataFrame but translate values to grid.
        {"grid_index": cell_idx, "area": area, "polygon": index[polygon_idx]}
    )
