import numpy as np
import pytest
from numpy.testing import assert_array_almost_equal

from lulucf import calculate_emissions


@pytest.mark.unittest
def test_calculate_emissions(somers_parcels, lasso_grid, simple_soilmap, bgt_gdf):
    flux, areal = calculate_emissions(
        somers_parcels, lasso_grid, simple_soilmap, bgt_gdf
    )
    nan = np.nan
    expected_flux = [
        [834.05040386, 836.18826335, 917.27213807, 1822.00449905],
        [1822.00449905, 917.27213807, 835.16359015, nan],
        [nan, 836.18826335, 1358.27582059, 1822.00449905],
        [1822.00449905, 1822.00449905, 836.18826335, 835.16359015],
    ]
    assert_array_almost_equal(flux, expected_flux)
