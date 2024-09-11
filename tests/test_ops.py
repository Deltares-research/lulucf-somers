import numpy as np
import pytest
from numpy.testing import assert_approx_equal, assert_array_equal

from lulucf.geometry import ops


@pytest.fixture
def ccw_polygon():
    return np.array([[1.5, 2.2], [1.2, 1.5], [1.9, 1.8], [2.5, 2.1], [1.5, 2.2]])


@pytest.fixture
def cw_polygon():
    return np.array([[0.9, 1.2], [0.9, 1.4], [1.4, 0.9], [1.2, 0.9], [0.9, 1.2]])


@pytest.fixture
def indices(ccw_polygon, cw_polygon):
    return np.repeat([0, 1], [len(ccw_polygon), len(cw_polygon)])


@pytest.fixture
def cell():
    return ops.Cell(1.0, 1.0, 2.0, 2.0)


@pytest.fixture
def polygon_collection(indices, ccw_polygon, cw_polygon):
    polygons = np.r_[ccw_polygon, cw_polygon]
    return ops.PolygonCoordinates(indices, polygons)


class TestPolygonCoordinates:
    @pytest.mark.unittest
    def test_select_index(self, polygon_collection):
        sel = polygon_collection.select_index(1)
        assert_array_equal(sel, [1, 1, 1, 1, 1])

    @pytest.mark.unittest
    def test_select_coordinates(self, polygon_collection):
        sel = polygon_collection.select_coordinates(1)
        expected_coords = [[0.9, 1.2], [0.9, 1.4], [1.4, 0.9], [1.2, 0.9], [0.9, 1.2]]
        assert_array_equal(sel, expected_coords)


class TestCell:
    @pytest.mark.unittest
    def test_get_cell_segments(self, cell):
        segments = cell.get_cell_segments()
        expected_segments = [[1, 1], [2, 1], [2, 2], [1, 2], [1, 1]]
        assert isinstance(segments, np.ndarray)
        assert_array_equal(segments, expected_segments)

        orient = ops.orientation(segments)
        assert orient == "ccw"

    @pytest.mark.unittest
    def test_contains_point(self, cell):
        assert cell.contains_point(1.5, 1.5)
        assert not cell.contains_point(4., 4.)


@pytest.mark.unittest
def test_polygon_area(ccw_polygon):
    area = ops.polygon_area(ccw_polygon)
    assert_approx_equal(area, 0.38)


@pytest.mark.unittest
def test_orientation_ccw(ccw_polygon):
    orient = ops.orientation(ccw_polygon)
    assert orient == "ccw"


@pytest.mark.unittest
def test_orientation_cw(cw_polygon):
    orient = ops.orientation(cw_polygon)
    assert orient == "cw"


@pytest.mark.unittest
def test_line_intersection():
    p1 = (1.0, 1.0)
    p2 = (2.0, 1.0)
    q1 = (1.0, 0.5)
    q2 = (2.0, 1.5)
    intersection = ops.line_intersection(p1, p2, q1, q2)
    assert intersection == (1.5, 1.0)

    q2 = (1.0, 0.5)
    intersection = ops.line_intersection(p1, p2, q1, q2)
    assert intersection is None


@pytest.mark.unittest
def test_clip_polygon(ccw_polygon, cell):
    result = ops.clip_polygon(ccw_polygon, cell)
    pass
