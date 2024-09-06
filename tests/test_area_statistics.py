import numpy as np
import pytest
from numpy.testing import assert_array_almost_equal

from lulucf.area_statistics import (
    _calc_percentage,
    calc_areal_percentage_in_cells,
    calc_areal_percentages_for,
)
from lulucf.utils import _add_layer_idx_column, cell_as_geometry


@pytest.fixture
def raster_cell():
    """
    Single raster cell to test _calc_percentage with.
    """
    return cell_as_geometry(0.5, 0.5, (1, 1))


@pytest.fixture
def grouped_soilmap(simple_soilmap):
    groups = np.repeat([0, 1, 2, 3], [5, 4, 4, 1])
    simple_soilmap["idx"] = groups
    return simple_soilmap


@pytest.mark.unittest
def test_calc_areal_percentage_in_cells(bgt_gdf, empty_bgt_array):
    bgt_gdf = _add_layer_idx_column(bgt_gdf, empty_bgt_array)

    result = calc_areal_percentage_in_cells(bgt_gdf, empty_bgt_array)

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
def test_calc_areal_percentages(
    bgt_gdf, grouped_soilmap, empty_bgt_array, empty_soilmap_array
):
    bgt_gdf = _add_layer_idx_column(bgt_gdf, empty_bgt_array)

    test_indices = [[1, 2], [2, 1]]
    bgt_da, soilmap_da = calc_areal_percentages_for(
        test_indices, bgt_gdf, grouped_soilmap, empty_bgt_array, empty_soilmap_array
    )

    expected_bgt_idx0 = [0, 0.11647059, 0.637315, 0, 0, 0.24621446, 0, 0, 0]
    expected_soilmap_idx0 = [1, 0, 0, 0]
    assert_array_almost_equal(bgt_da[1, 2], expected_bgt_idx0)
    assert_array_almost_equal(soilmap_da[1, 2], expected_soilmap_idx0)

    expected_bgt_idx1 = [0, 0, 0.15508972, 0.40695038, 0.4073349, 0.030625, 0, 0, 0]
    expected_soilmap_idx1 = [0.15508972, 0.4379599, 0.40695038, 0]
    assert_array_almost_equal(bgt_da[2, 1], expected_bgt_idx1)
    assert_array_almost_equal(soilmap_da[2, 1], expected_soilmap_idx1)


@pytest.mark.unittest
def test_calc_percentage(raster_cell, grouped_soilmap):
    ngroups = 4
    cellarea = 1
    perc = _calc_percentage(raster_cell, grouped_soilmap, cellarea, ngroups)
    expected_result = [0, 0.84455372, 0.03044628, 0.125]
    assert_array_almost_equal(perc, expected_result)
