import sqlite3
from pathlib import WindowsPath

import geopandas as gpd
import numpy as np
import pandas as pd
import xarray as xr
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
