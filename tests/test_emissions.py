import numpy as np
import pytest
from numpy.testing import assert_array_almost_equal

from lulucf import calculate_somers_emissions


@pytest.mark.unittest
def test_calculate_emissions(somers_parcels, lasso_grid):
    flux = calculate_somers_emissions(somers_parcels, lasso_grid)
    nan = np.nan
    expected_flux = [
        [0.15130456, 0.25254545, 0.27000692, 0.225],
        [0.15, 0.44157245, 0.60202263, nan],
        [nan, 0.62484131, 0.44101893, 0.33260913],
        [0.48014338, 0.7, 0.358, 0.42597532],
    ]
    assert_array_almost_equal(flux, expected_flux)
