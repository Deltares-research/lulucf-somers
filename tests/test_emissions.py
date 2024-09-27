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
        [0.08340504, 0.08361883, 0.09172721, 0.18220045],
        [0.18220045, 0.09172721, 0.08351636, nan],
        [nan, 0.08361883, 0.13582758, 0.18220045],
        [0.18220045, 0.18220045, 0.08361883, 0.08351636],
    ]
    assert_array_almost_equal(flux, expected_flux)
