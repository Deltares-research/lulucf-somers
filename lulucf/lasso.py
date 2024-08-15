import numpy as np
import xarray as xr


class Lasso:
    """
    Containing definition of Lasso grid (25x25 m resolution?). This is the basic grid all
    the calculations will be performed in and the results will be generated for.

    """
    xmin: float = 13591.500074
    xmax: float = 278041.500074
    ymin: float = 306882.749948
    ymax: float = 619107.749948
    xsize: int = 25
    ysize: int = 25
    
    def dataarray(self):
        xcoords = np.arange(self.xmin, self.xmax + self.xsize, self.xsize)
        ycoords = np.arange(self.ymax, self.ymin - self.ysize, -self.ysize)

        coords = {'y': ycoords, 'x': xcoords}
        size = (len(ycoords), len(xcoords))
        return xr.DataArray(np.full(size, 1), coords=coords, dims=('y', 'x'))


if __name__ == "__main__":
    lasso = Lasso()
    da = lasso.dataarray()
    print(2)
    