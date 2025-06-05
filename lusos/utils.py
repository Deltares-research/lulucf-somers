import cProfile
import sqlite3
from functools import wraps
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import xarray as xr
from rasterio import features
from shapely.geometry import Polygon, box


def cell_as_geometry(
    xcell: int | float, ycell: int | float, cellsize: tuple
) -> Polygon:
    """
    Create a bounding box Polygon of a raster cell from the "x" and "y" coordinate of a
    cell center and the cellsize of the cell.

    Parameters
    ----------
    xcell, ycell : int | float
        X- and y-coordinate of the cell center.
    cellsize : tuple (xsize, ysize)
        Tuple containing the xsize and ysize of the cell.

    Returns
    -------
    Polygon
        Polygon of the bounding box of the cell.

    """
    xsize, ysize = cellsize

    dy = np.abs(0.5 * ysize)
    dx = np.abs(0.5 * xsize)

    ymin, ymax = ycell - dy, ycell + dy
    xmin, xmax = xcell - dx, xcell + dx

    return box(xmin, ymin, xmax, ymax)


def _add_layer_idx_column(gdf: gpd.GeoDataFrame, layers: list):
    """
    Helper function to add the index of the layer coordinates in a DataArray to a
    GeoDataFrame.

    """
    df = pd.DataFrame(layers, columns=["layer"])
    df.index.name = "idx"
    df.reset_index(inplace=True)
    gdf = gdf.merge(df, on="layer", how="left")
    return gdf


def create_connection(database: str | Path):
    """
    Create a database connection to an SQLite database.

    Parameters
    ----------
    database: string
        Path/url/etc. to the database to create the connection to.

    Returns
    -------
    conn : sqlite3.Connection
        Connection object or None.

    """
    conn = None
    try:
        conn = sqlite3.connect(database)
    except sqlite3.Error as e:
        print(e)

    return conn


def profile_function(func):  # pragma: no cover
    @wraps(func)
    def wrapper(*args, **kwargs):
        profiler = cProfile.Profile()
        profiler.enable()
        result = func(*args, **kwargs)
        profiler.disable()
        profiler.print_stats(sort="cumulative")
        return result

    return wrapper


def rasterize_like(
    shapefile: str | Path | gpd.GeoDataFrame,
    da: xr.DataArray,
    attribute: str = None,
    **features_kwargs,
):
    """
    Rasterize a shapefile like an Xarray DataArray object.

    Parameters
    ----------
    shapefile : str | Path | gpd.GeoDataFrame
        Input shapefile to rasterize. Can be a path to the shapefile or an in
        memory GeoDataFrame.
    da : xr.DataArray,
        DataArray to use the extent from rasterize the shapefile like.
    attribute : str, optional
        Name of the attribute in the shapefile to rasterize. The default is None, in
        this case, a default value of 1 will be burnt into the DataArray.

    **features_kwargs
        See rasterio.features.rasterize docs for additional optional parameters.

    Returns
    -------
    xr.DataArray
        DataArray of the rasterized shapefile.

    Examples
    --------
    Rasterize a specific attribute of a shapefile:
    >>> rasterize_like(shapefile, da, "attribute")

    Use additional `features.rasterize` options:
    >>> rasterize_like(shapefile, da, "attribute", fill=np.nan, all_touched=True)

    """
    if isinstance(shapefile, (str, Path)):
        shapefile = gpd.read_file(shapefile)

    if attribute:
        shapes = (
            (geom, z) for z, geom in zip(shapefile[attribute], shapefile["geometry"])
        )
    else:
        shapes = (geom for geom in shapefile["geometry"])
        features_kwargs["default_value"] = 1

    rasterized = features.rasterize(
        shapes=shapes,
        out_shape=da.shape,
        transform=da.rio.transform(),
        **features_kwargs,
    )

    return xr.DataArray(rasterized, coords=da.coords, dims=da.dims)


def rasterize_as_mask(
    shapefile: str | Path | gpd.GeoDataFrame,
    da: xr.DataArray,
    **features_kwargs,
):
    """
    Rasterize a shapefile as a boolean mask within the extent of an Xarray DataArray
    object. By default, mask is intended for use as a numpy mask, where cells that
    overlap shapefile geometries are False.

    Parameters
    ----------
    shapefile : str | Path | gpd.GeoDataFrame
        Input shapefile to rasterize. Can be a path to the shapefile or an in
        memory GeoDataFrame.
    da : xr.DataArray,
        DataArray to use the extent from rasterize the shapefile like.

    **features_kwargs
        See rasterio.features.rasterize docs for additional optional parameters.

    Returns
    -------
    xr.DataArray
        Boolean DataArray of the rasterized shapefile.

    Examples
    --------
    Get a default mask (i.e. where cells that overlap with geometries are False):
    >>> rasterize_as_mask(shapefile, da)

    Get a mask which is True for cells that overlap with geometries:
    >>> rasterize_as_mask(shapefile, da, invert=True)

    """
    if isinstance(shapefile, (str, Path)):
        shapefile = gpd.read_file(shapefile)

    shapes = (geom for geom in shapefile["geometry"])

    mask = features.geometry_mask(
        geometries=shapes,
        out_shape=da.shape,
        transform=da.rio.transform(),
        **features_kwargs,
    )

    return xr.DataArray(mask, coords=da.coords, dims=da.dims)


def get_valid_indices(mask: np.ndarray | xr.DataArray) -> np.ndarray:
    """
    Return the indices where a boolean array or DataArray is True.

    Parameters
    ----------
    mask : np.ndarray | xr.DataArray
        Boolean array to find the indices from.

    Returns
    -------
    np.ndarray
        Array of shape (n, 2) containing the indices where the boolean array is True.

    """
    if isinstance(mask, xr.DataArray):
        mask = mask.values
    return np.argwhere(mask)
