import numpy as np
import pytest
import xarray as xr
from numpy.testing import assert_array_almost_equal, assert_array_equal

from lusos import bgt_soilmap_coverage


@pytest.mark.unittest
def test_bgt_soilmap_coverage(bgt_gdf, simple_soilmap, lasso_grid):
    simple_soilmap["soilunit_sequencenumber"] = 1  # Add for _prepare_soilmap
    coverage = bgt_soilmap_coverage(bgt_gdf, simple_soilmap, lasso_grid)
    assert isinstance(coverage, xr.DataArray)
    assert coverage.dims == ("y", "x", "layer")
    assert coverage.sizes == {"y": 4, "x": 4, "layer": 36}

    # One cell is covered by other and missing from calculation result
    assert np.isclose(coverage.sum(), 15.875)

    assert_array_equal(
        coverage["layer"],
        [
            "percelen_peat",
            "overig_groen_peat",
            "stedelijk_groen_peat",
            "openbare_ruimte_peat",
            "panden_peat",
            "erven_peat",
            "sloten_peat",
            "grote_wateren_peat",
            "overig_peat",
            "percelen_moerig",
            "overig_groen_moerig",
            "stedelijk_groen_moerig",
            "openbare_ruimte_moerig",
            "panden_moerig",
            "erven_moerig",
            "sloten_moerig",
            "grote_wateren_moerig",
            "overig_moerig",
            "percelen_buried",
            "overig_groen_buried",
            "stedelijk_groen_buried",
            "openbare_ruimte_buried",
            "panden_buried",
            "erven_buried",
            "sloten_buried",
            "grote_wateren_buried",
            "overig_buried",
            "percelen_buried_deep",
            "overig_groen_buried_deep",
            "stedelijk_groen_buried_deep",
            "openbare_ruimte_buried_deep",
            "panden_buried_deep",
            "erven_buried_deep",
            "sloten_buried_deep",
            "grote_wateren_buried_deep",
            "overig_buried_deep",
        ],
    )
    expected_idx0 = [0.0153125, 0, 0.23090196, 0.11647059, 0, 0, 0.63731498] + [0] * 29
    assert_array_almost_equal(coverage[1, 2], expected_idx0)

    expected_idx1 = (
        [0.00474962, 0, 0.06311382, 0, 0, 0]
        + [0.08722627, 0, 0, 0.01341252, 0, 0.17822795]
        + [0, 0, 0, 0.24631943, 0, 0]
        + [0.01246286, 0, 0.16560862, 0, 0, 0, 0.22887891]
        + [0] * 11
    )
    assert_array_almost_equal(coverage[2, 1], expected_idx1)
