import pytest

from lulucf.lasso import LassoGrid


@pytest.fixture
def lasso_grid() -> LassoGrid:
    """
    LassoGrid instance with simple bounds.

    """
    xmin, xmax = 0, 4
    ymin, ymax = 0, 4
    cellsize = 1
    return LassoGrid(xmin, ymin, xmax, ymax, cellsize, cellsize)


@pytest.fixture
def raster_file(lasso_grid, tmp_path):
    """
    Temporary raster file from the lasso_grid fixture.

    """
    outfile = tmp_path / r"temp.tif"
    da = lasso_grid.dataarray()
    da.rio.to_raster(outfile)
    return outfile
