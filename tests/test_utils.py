import sqlite3

import numpy as np
import pytest
from numpy.testing import assert_array_equal
from shapely.geometry import Polygon

from lulucf.utils import cell_as_geometry, create_connection, rasterize_like


@pytest.fixture
def cellsize_negative_y():
    return (1, -1)


@pytest.fixture
def cellsize_negative_x():
    return (-1, 1)


@pytest.fixture
def cellsize_positive():
    return (1, 1)


@pytest.mark.parametrize(
    "cellsize", ["cellsize_negative_y", "cellsize_negative_x", "cellsize_positive"]
)
def test_cell_as_geometry(cellsize, request):
    cellsize = request.getfixturevalue(cellsize)

    xcell = 1.5
    ycell = 1.5

    geom = cell_as_geometry(xcell, ycell, cellsize)

    assert isinstance(geom, Polygon)
    assert geom.bounds == (1, 1, 2, 2)


@pytest.mark.unittest
def test_create_connection(simple_soilmap_path):
    conn = create_connection(simple_soilmap_path)
    assert isinstance(conn, sqlite3.Connection)


@pytest.mark.unittest
def test_rasterize_like(lasso_grid, somers_parcels):
    da = lasso_grid.dataarray()

    raster = rasterize_like(somers_parcels, "parcel_id", da)

    expected_values = [
        [0, np.nan, 4, 4],
        [1, 1, 4, 4],
        [np.nan, np.nan, 2, np.nan],
        [np.nan, 3, 3, np.nan],
    ]

    assert raster.shape == (4, 4)
    assert raster.rio.bounds() == (0, 0, 4, 4)
    assert raster.rio.resolution() == (1, -1)
    assert raster.sizes == {'y': 4, 'x': 4}
    assert_array_equal(raster.values, expected_values)
