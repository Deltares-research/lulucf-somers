import cProfile
import sqlite3
from functools import wraps
from pathlib import WindowsPath

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


def _add_layer_idx_column(gdf: gpd.GeoDataFrame, da: xr.DataArray):
    """
    Helper function to add the index of the layer coordinates in a DataArray to a
    GeoDataFrame.

    """
    df = pd.DataFrame(da["layer"].values, columns=["layer"])
    df.index.name = "idx"
    df.reset_index(inplace=True)
    gdf = gdf.merge(df, on="layer", how="left")
    return gdf


def create_connection(database: str | WindowsPath):
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


def profile_function(func):
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
    shapefile: str | WindowsPath | gpd.GeoDataFrame,
    attribute: str,
    da: xr.DataArray,
):
    """
    Rasterize a shapefile like an atmod Raster or into the 2D extent of a VoxelModel
    object.

    Parameters
    ----------
    shapefile : str | WindowsPath | gpd.GeoDataFrame
        Input shapefile to rasterize. Can be a path to the shapefile or an in
        memory GeoDataFrame.
    attribute : str
        Name of the attribute in the shapefile to rasterize.
    da : xr.DataArray,
        Atmod Raster or VoxelModel object to rasterize the shapefile like.
    cellsize : int, optional
        Cellsize of the output DataArray. The default is None, then the x and y
        size will be derived from the input DataArray.

    Returns
    -------
    xr.DataArray
        DataArray of the rasterized shapefile.

    """
    if isinstance(shapefile, (str, WindowsPath)):
        shapefile = gpd.read_file(shapefile)

    shapes = ((geom, z) for z, geom in zip(shapefile[attribute], shapefile["geometry"]))

    rasterized = features.rasterize(
        shapes=shapes,
        fill=np.nan,
        out_shape=da.shape,
        transform=da.rio.transform(),
    )
    rasterized = xr.DataArray(rasterized, coords=da.coords, dims=da.dims)
    return rasterized
