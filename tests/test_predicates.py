import numpy as np
import pytest
from numpy.testing import assert_array_equal

from lulucf.geometry import predicates


@pytest.fixture
def cell():
    return 1, 1, 2, 2


@pytest.fixture
def bounds():
    return np.array(
        [
            [1.5, 1.5, 2.5, 2.5],  # Overlaps
            [0.5, 0.5, 2.5, 2.5],  # Contains
            [1.25, 1.25, 1.75, 1.75],  # Within
            [3, 3, 4, 4],  # Completely outside
        ]
    )


@pytest.mark.unittest
def test_bbox_overlaps_cell(cell, bounds):
    xmin, ymin, xmax, ymax = cell
    overlap = predicates.bbox_overlaps_cell(xmin, ymin, xmax, ymax, bounds)
    assert_array_equal(overlap, [True, True, False, False])


@pytest.mark.unittest
def test_bbox_within_cell(cell, bounds):
    xmin, ymin, xmax, ymax = cell
    overlap = predicates.bbox_within_cell(xmin, ymin, xmax, ymax, bounds)
    assert_array_equal(overlap, [False, False, True, False])


@pytest.mark.unittest
def test_bbox_contains_cell(cell, bounds):
    xmin, ymin, xmax, ymax = cell
    overlap = predicates.bbox_contains_cell(xmin, ymin, xmax, ymax, bounds)
    assert_array_equal(overlap, [False, True, False, False])


@pytest.mark.unittest
def test_get_overlapping_polygons(cell, bounds):
    xmin, ymin, xmax, ymax = cell
    overlap = predicates.get_overlapping_polygons(xmin, ymin, xmax, ymax, bounds)
    assert_array_equal(overlap, [True, True, True, False])
