import numpy as np
import pytest
from numpy.testing import assert_array_almost_equal, assert_array_equal

from lusos.area_statistics import (
    _weighted_average,
    area_to_grid3d,
    calc_areal_percentage_in_cells,
)
from lusos.constants import MAIN_BGT_UNITS
from lusos.geometry.ops import PolygonGridArea
from lusos.utils import _add_layer_idx_column


@pytest.fixture
def area_tuple():
    return PolygonGridArea(
        np.array([12]), np.array([2]), np.array([0, 0]), np.array([0.5, 0.5])
    )


@pytest.fixture
def grouped_soilmap(simple_soilmap):
    simple_soilmap["layer"] = np.repeat(
        ["peat", "moerig", "buried", "other"], [5, 4, 4, 1]
    )
    simple_soilmap["idx"] = np.repeat([0, 1, 2, 3], [5, 4, 4, 1])
    return simple_soilmap


@pytest.fixture
def grouped_bgt(bgt_gdf):
    bgt_gdf["layer"] = [
        "percelen",
        "openbare_ruimte",
        "stedelijk_groen",
        "openbare_ruimte",
        "sloten",
        "panden",
        "percelen",
        "overig_groen",
        "sloten",
        "stedelijk_groen",
        "percelen",
        "overig",
        "overig_groen",
        "overig",
    ]
    bgt_gdf = _add_layer_idx_column(bgt_gdf, MAIN_BGT_UNITS)
    return bgt_gdf


@pytest.mark.unittest
def test_calc_areal_percentage_in_cells(grouped_bgt, lasso_grid):
    result = calc_areal_percentage_in_cells(grouped_bgt, lasso_grid, MAIN_BGT_UNITS)

    assert np.all((result == 0).any(dim="layer"))

    # Test result at sample locations.
    assert_array_almost_equal(
        result[0, 0], [0.00660393, 0.39253831, 0, 0.60085773, 0, 0, 0, 0, 0]
    )
    assert_array_almost_equal(
        result[0, 1], [0.85454547, 0, 0, 0.14545454, 0, 0, 0, 0, 0]
    )
    assert_array_almost_equal(result[3, 2], [0.1, 0, 0, 0, 0.9, 0, 0, 0, 0])


@pytest.mark.unittest
def test_area_to_grid3d(area_tuple):
    nan = np.nan
    grid = np.full((4, 4, 1), nan)
    grid = area_to_grid3d(area_tuple, grid)

    expected_grid = [
        [[nan], [nan], [nan], [nan]],
        [[nan], [nan], [nan], [nan]],
        [[nan], [nan], [nan], [nan]],
        [[1], [nan], [nan], [nan]],
    ]
    assert_array_equal(grid, expected_grid)


@pytest.mark.unittest
def test_weighted_average():
    values = np.array([1, 2])
    weights = np.array([2, 3])
    assert _weighted_average(values, weights) == 1.6
