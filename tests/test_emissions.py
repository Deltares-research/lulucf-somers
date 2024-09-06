import numpy as np
import pytest
from numpy.testing import assert_array_almost_equal

from lulucf.emissions import calculate_emissions


@pytest.mark.unittest
def test_calculate_emissions(somers_parcels, lasso_grid, simple_soilmap, bgt_gdf):
    flux, areal = calculate_emissions(
        somers_parcels, lasso_grid, simple_soilmap, bgt_gdf, False
    )
    nan = np.nan
    expected_flux = [
        [1513.04561724, 2525.45454545, 2700.06923526, nan],
        [1500., 4415.72445438, 6020.22630994, nan],
        [nan, nan, 4410.18934408, nan],
        [nan, 7000., 3580., 4259.75316917]
    ]
    assert_array_almost_equal(flux, expected_flux)

    invalid_indices = np.isnan(flux)
    assert np.all(areal.values[invalid_indices.values]==0)

    valid_values = areal.values[~invalid_indices.values]
    assert np.all(valid_values >= 0)
    assert np.any(valid_values > 0)
