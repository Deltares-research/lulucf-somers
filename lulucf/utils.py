import numpy as np
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
