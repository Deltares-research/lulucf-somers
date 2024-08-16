from pathlib import Path

import numpy as np
import pytest
import xarray as xr
from numpy.testing import assert_array_equal
from shapely.geometry import Polygon

from lulucf.lasso import LassoGrid
from lulucf.preprocessing.bgt import BGT_LAYERS_FOR_LULUCF


class TestLassoGrid:
    @pytest.mark.unittest
    def test_initialize_wrong_xy_size(self):
        wrong_xsize = -1
        wrong_ysize = 1
        lasso = LassoGrid(0, 0, 4, 4, wrong_xsize, wrong_ysize)

        assert lasso.xsize == 1
        assert lasso.ysize == -1

    @pytest.mark.unittest
    def test_xcoordinates(self, lasso_grid):
        xco = lasso_grid.xcoordinates()
        expected_xco = [0.5, 1.5, 2.5, 3.5]
        assert_array_equal(xco, expected_xco)

    @pytest.mark.unittest
    def test_ycoordinates(self, lasso_grid):
        yco = lasso_grid.ycoordinates()
        expected_yco = [3.5, 2.5, 1.5, 0.5]
        assert_array_equal(yco, expected_yco)

    @pytest.mark.unittest
    def test_dataarray(self, lasso_grid):
        da = lasso_grid.dataarray()

        assert isinstance(da, xr.DataArray)
        assert len(da["x"]) == 4
        assert len(da["y"]) == 4
        assert da.rio.resolution() == (1.0, -1.0)
        assert da.rio.crs == 28992

    @pytest.mark.unittest
    def test_from_raster(self, raster_file):
        grid = LassoGrid.from_raster(raster_file)

        assert grid.xmin == 0
        assert grid.ymin == 0
        assert grid.xmax == 4
        assert grid.ymax == 4
        assert grid.xsize == 1
        assert grid.ysize == -1
        assert grid.crs == 28992

    @pytest.mark.unittest
    def test_empty_array(self):
        layers = [layer.replace("_polygon", "") for layer in BGT_LAYERS_FOR_LULUCF]

        grid = LassoGrid(0, 300_000, 280_000, 625_000, 25, 25)
        da = grid.empty_array(layers)

        assert isinstance(da, xr.DataArray)
        assert da.shape == (13_000, 11_200, 9)
        assert da.dims == ("y", "x", "layer")
        assert da.chunks is not None

        grid = LassoGrid(0, 0, 1000, 1000, 25, 25)
        da = grid.empty_array(layers, dask=False)

        assert da.shape == (40, 40, 9)
        assert da.dims == ("y", "x", "layer")
        assert da.chunks is None
        assert np.all(da == 0)
