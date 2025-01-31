import geopandas as gpd
import numpy as np
import pytest
from numpy.testing import assert_array_almost_equal, assert_array_equal
from shapely.geometry import box

from lusos.geometry import ops


@pytest.fixture
def polygon_gdf():
    outer = box(0, 0, 1, 1)
    inner = box(0.3, 0.3, 0.7, 0.7)
    outer = outer.difference(inner)
    return gpd.GeoDataFrame(geometry=[inner, outer])


@pytest.mark.unittest
def test_triangulate(polygon_gdf):
    triangles, index, coords = ops.triangulate(polygon_gdf)
    assert_array_equal(
        triangles,
        [
            [3, 0, 1],
            [1, 2, 3],
            [9, 12, 11],
            [13, 12, 9],
            [6, 9, 11],
            [13, 9, 8],
            [7, 6, 11],
            [14, 13, 8],
            [7, 11, 14],
            [14, 8, 7],
        ],
    )
    assert_array_equal(index, [0, 0, 1, 1, 1, 1, 1, 1, 1, 1])
    assert_array_equal(
        coords,
        [
            [0.7, 0.3],
            [0.7, 0.7],
            [0.3, 0.7],
            [0.3, 0.3],
            [0.7, 0.3],
            [0.0, 0.0],
            [0.0, 1.0],
            [1.0, 1.0],
            [1.0, 0.0],
            [0.0, 0.0],
            [0.7, 0.7],
            [0.3, 0.7],
            [0.3, 0.3],
            [0.7, 0.3],
            [0.7, 0.7],
        ],
    )


@pytest.mark.unittest
def test_polygon_area_in_grid(polygon_gdf, lasso_grid):
    area = ops.polygon_area_in_grid(polygon_gdf, lasso_grid.dataarray())
    assert_array_equal(area.cell_idx, [12])
    assert_array_equal(area.cell_indices, [10])
    assert_array_equal(area.polygon, [1, 1, 1, 1, 0, 0, 1, 1, 1, 1])
    assert_array_almost_equal(
        area.area, [0.06, 0.15, 0.15, 0.06, 0.08, 0.08, 0.06, 0.15, 0.06, 0.15]
    )
    assert np.isclose(area.area.sum(), 1)
