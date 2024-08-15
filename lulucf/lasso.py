from pathlib import WindowsPath

import numpy as np
import rioxarray as rio
import xarray as xr
from pyproj import CRS


class LassoGrid:
    """
    Containing definition of Lasso grid (25x25 m resolution?). This is the basic grid all
    the calculations will be performed in and the results will be generated for.
    """

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
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax

        if xsize < 0:
            xsize *= -1
        self.xsize = xsize

        if ysize > 0:
            ysize *= -1
        self.ysize = ysize
        self.crs = CRS(crs)

    @classmethod
    def from_raster(cls, raster: str | WindowsPath):
        raster = rio.open_rasterio(raster).squeeze()
        xsize, ysize = raster.rio.resolution()
        xmin, ymin, xmax, ymax = raster.rio.bounds()
        return cls(xmin, ymin, xmax, ymax, xsize, ysize)

    def xcoordinates(self):
        xmin = self.xmin + 0.5 * self.xsize
        return np.arange(xmin, self.xmax, self.xsize)

    def ycoordinates(self):
        ymax = self.ymax + 0.5 * self.ysize
        return np.arange(ymax, self.ymin, self.ysize)

    def dataarray(self) -> xr.DataArray:
        ycoords, xcoords = self.ycoordinates(), self.xcoordinates()
        coords = {"y": ycoords, "x": xcoords}
        size = (len(ycoords), len(xcoords))
        da = xr.DataArray(np.full(size, 1), coords=coords, dims=("y", "x"))
        return da.rio.write_crs(self.crs, inplace=True)
