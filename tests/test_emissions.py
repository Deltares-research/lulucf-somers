import numpy as np
import pytest
from numpy.testing import assert_array_almost_equal

from lulucf import calculate_somers_emissions


@pytest.mark.unittest
def test_calculate_emissions(somers_parcels, lasso_grid):
    flux = calculate_somers_emissions(somers_parcels, lasso_grid)
    nan = np.nan
    expected_flux = [
        [0.08340504, 0.16767227, 0.18220442, 0.55555556],
        [0.0823192, 0.27157892, 0.3724996, nan],
        [nan, 0.43247482, 0.26455175, 0.21827676],
        [3.83796201, 0.71304406, 0.22566407, 0.5645628],
    ]
    assert_array_almost_equal(flux, expected_flux)
