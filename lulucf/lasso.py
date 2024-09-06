from pathlib import WindowsPath

import dask.array as darray
import numpy as np
import rioxarray as rio
import xarray as xr
from pyproj import CRS

from lulucf.validation import LassoValidator


class LassoGrid:
    """
    Containing definition of LASSO grid (25x25 m resolution?). This is the basic grid all
    the calculations will be performed in and the results will be generated for.

    Parameters
    ----------
    xmin, ymin, xmax, ymax : int | float
        Bounding box coordinates of the LASSO grid.
    xsize, ysize : int
        Cellsize in x- and y-direction of the LASSO grid.
    crs : str | int | CRS
        EPSG of the target crs. Takes anything that can be interpreted by
        pyproj.crs.CRS.from_user_input().

    """

    def __new__(cls, *args):
        validator = LassoValidator()
        validator.validate(*args)
        return super().__new__(cls)

    def __init__(
        self,
        xmin: int | float,
        ymin: int | float,
        xmax: int | float,
        ymax: int | float,
        xsize: int,
        ysize: int,
        crs: str | int | CRS = 28992,
    ):
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax

        self.xsize = xsize * -1 if xsize < 0 else xsize
        self.ysize = ysize * -1 if ysize > 0 else ysize

        self.crs = CRS(crs)

    def __repr__(self):
        name = self.__class__.__name__
        xmin, ymin, xmax, ymax = self.xmin, self.ymin, self.xmax, self.ymax
        xsize, ysize = self.xsize, self.ysize
        return f"{name}({xmin=}, {ymin=}, {xmax=}, {ymax=}, {xsize=}, {ysize=})"

    @classmethod
    def from_raster(cls, raster: str | WindowsPath):
        """
        Initialize a LassoGrid instance from a raster file.

        Parameters
        ----------
        raster : str | WindowsPath
            Path to the raster file to base the grid extent on.

        """
        raster = rio.open_rasterio(raster).squeeze()
        xsize, ysize = raster.rio.resolution()
        xmin, ymin, xmax, ymax = raster.rio.bounds()
        return cls(xmin, ymin, xmax, ymax, xsize, ysize)

    def xcoordinates(self):
        """
        Return an array of increasing x-coordinates of the LASSO grid.
        """
        xmin = self.xmin + 0.5 * self.xsize
        return np.arange(xmin, self.xmax, self.xsize)

    def ycoordinates(self):
        """
        Return an array of decreasing y-coordinates of the LASSO grid.
        """
        ymax = self.ymax - np.abs(0.5 * self.ysize)
        return np.arange(ymax, self.ymin, self.ysize)

    def dataarray(self, fill_value: int | float = 1) -> xr.DataArray:
        """
        Return a 2D DataArray filled with a single value with the full extent of the LASSO
        grid.

        Parameters
        ----------
        fill_value : int | float, optional
            Value to use in the DataArray. The default is 1.

        Returns
        -------
        xr.DataArray

        """
        ycoords, xcoords = self.ycoordinates(), self.xcoordinates()
        coords = {"y": ycoords, "x": xcoords}
        size = (len(ycoords), len(xcoords))
        da = xr.DataArray(
            np.full(size, fill_value, dtype=type(fill_value)),
            coords=coords,
            dims=("y", "x"),
        )
        return da.rio.write_crs(self.crs, inplace=True)

    def empty_array(
        self, layer_coords: list, dask: bool = True, chunksize: int = 3100
    ) -> xr.DataArray:
        """
        Create an empty 3D DataArray within the extent of the LASSO grid. The "layer_coords"
        are added in the 3rd dimension, "layer", of the DataArray.

        Parameters
        ----------
        layer_coords : list
            List of coordinate names of the "layer" dimension.
        dask : bool, optional
            If True, a DataArray containing an empty Dask array is returned otherwise, a
            DataArray containing all zeros is returned. The default is True.
        chunksize : int, optional
            If the Dask option is used, specify a chunk size for the "y" and "x" dimensions.
            The dimension "layer" is handled as a single chunk. Recommended memory size of
            chunks is approximately 100 MB (see Dask documentation). The default is 3100.

        Returns
        -------
        xr.DataArray
            Empty DataArray.

        """
        x = self.xcoordinates()
        y = self.ycoordinates()

        ny, nx, nz = len(y), len(x), len(layer_coords)

        if dask:
            empty_arr = darray.empty(
                shape=(ny, nx, nz), dtype="float32", chunks=(chunksize, chunksize, nz)
            )
        else:
            empty_arr = np.full((ny, nx, nz), 0.0, dtype="float32")

        coords = {"y": y, "x": x, "layer": layer_coords}
        return xr.DataArray(empty_arr, coords)
