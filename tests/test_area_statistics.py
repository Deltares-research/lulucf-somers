import numpy as np
import pytest
from numpy.testing import assert_array_almost_equal

from lulucf.area_statistics import calc_areal_percentage_in_cells
from lulucf.utils import _add_layer_idx_column


@pytest.mark.unittest
def test_calc_areal_percentage_in_cells(bgt_gdf, empty_bgt_array):
    bgt_gdf = _add_layer_idx_column(bgt_gdf, empty_bgt_array)

    result = calc_areal_percentage_in_cells(bgt_gdf, empty_bgt_array)

    assert np.all((result == 0).any(dim="layer"))

    # Test result at sample locations.
    assert_array_almost_equal(
        result[0, 0], [0.00660393, 0.60085776, 0, 0.39253831, 0, 0, 0, 0, 0]
    )
    assert_array_almost_equal(
        result[0, 1], [0.85454545, 0.14545455, 0, 0, 0, 0, 0, 0, 0]
    )
    assert_array_almost_equal(result[3, 2], [0, 0, 0, 0, 0, 0.9, 0.1, 0, 0])


@pytest.mark.unittest
def test_calc_areal_percentages(
    bgt_gdf, simple_soilmap, empty_bgt_array, empty_soilmap_array
):
    assert 1 == 1
