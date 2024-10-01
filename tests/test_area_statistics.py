import numpy as np
import pytest
from numpy.testing import assert_array_almost_equal, assert_array_equal

from lulucf.area_statistics import (
    area_to_grid3d,
    areal_percentage_bgt_soilmap,
    calc_areal_percentage_in_cells,
)
from lulucf.emissions import (
    MAIN_BGT_UNITS,
    MAIN_SOILMAP_UNITS,
)
from lulucf.geometry.ops import PolygonGridArea
from lulucf.utils import _add_layer_idx_column


@pytest.fixture
def area_tuple():
    return PolygonGridArea([12], [2], [0, 0], [0.5, 0.5])


@pytest.fixture
def grouped_soilmap(simple_soilmap):
    simple_soilmap["layer"] = np.repeat(
        ["peat", "moerig", "buried", "other"], [5, 4, 4, 1]
    )
    simple_soilmap["idx"] = np.repeat([0, 1, 2, 3], [5, 4, 4, 1])
    return simple_soilmap


@pytest.mark.unittest
def test_calc_areal_percentage_in_cells(bgt_gdf, lasso_grid):
    bgt_gdf = _add_layer_idx_column(bgt_gdf, MAIN_BGT_UNITS)

    result = calc_areal_percentage_in_cells(bgt_gdf, lasso_grid, MAIN_BGT_UNITS)

    assert np.all((result == 0).any(dim="layer"))

    # Test result at sample locations.
    assert_array_almost_equal(
        result[0, 0], [0, 0, 0, 0, 0, 0.39914224, 0.60085773, 0, 0]
    )
    assert_array_almost_equal(
        result[0, 1], [0, 0, 0, 0, 0, 0.8545455, 0.14545455, 0, 0]
    )
    assert_array_almost_equal(result[3, 2], [0.9, 0, 0, 0, 0, 0.1, 0, 0, 0])


@pytest.mark.unittest
def test_areal_percentage_bgt_soilmap(lasso_grid, bgt_gdf, grouped_soilmap):
    bgt_gdf = _add_layer_idx_column(bgt_gdf, MAIN_BGT_UNITS)

    areal = areal_percentage_bgt_soilmap(
        lasso_grid, bgt_gdf, grouped_soilmap, MAIN_BGT_UNITS, MAIN_SOILMAP_UNITS
    )
    areal = areal.reshape(4, 4, 36)
    expected_idx0 = [0, 0.11647059, 0.637315, 0, 0, 0.24621446] + [0] * 30
    assert_array_almost_equal(areal[1, 2], expected_idx0)

    expected_idx1 = (
        [0] * 2
        + [0.02405282, 0.06311382, 0.06317346, 0.00474962]
        + [0] * 5
        + [0.06792308, 0.17822795, 0.17839636, 0.01341252]
        + [0] * 5
        + [0.06311382, 0.16560861, 0.16576509, 0.01246286]
        + [0] * 12
    )
    assert_array_almost_equal(areal[2, 1], expected_idx1)


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
