import geopandas as gpd
import numpy as np
import pytest
from numpy.testing import assert_array_equal
from shapely.geometry import box

from lulucf.geometry import ops


@pytest.fixture
def gdf_single_polygon():
    return gpd.GeoDataFrame(geometry=[box(0, 0, 1, 1)])


@pytest.mark.unittest
def test_polygon_vertices(gdf_single_polygon):
    coords, index = ops.polygon_coords(gdf_single_polygon)
    expected_coords = [[1, 0], [1, 1], [0, 1], [0, 0], [1, 0]]
    assert_array_equal(coords, expected_coords)
    assert_array_equal(index, [0, 0, 0, 0, 0])


@pytest.mark.unittest
def test_triangulate():
    coords = [[1, 0], [1, 1], [0, 1], [0, 0], [1, 0]]
    index = [0, 0, 0, 0, 0]
    triangles, index = ops.triangulate(coords, index)
    assert_array_equal(triangles, [[3, 0, 1], [1, 2, 3]])
    assert_array_equal(index, [0, 0])


@pytest.mark.unittest
def test_polygon_area_in_grid(gdf_single_polygon, lasso_grid):
    area = ops.polygon_area_in_grid(gdf_single_polygon, lasso_grid.dataarray())
    assert_array_equal(area.cell_idx, [12])
    assert_array_equal(area.cell_indices, [2])
    assert_array_equal(area.polygon, [0, 0])
    assert_array_equal(area.area, [0.5, 0.5])
