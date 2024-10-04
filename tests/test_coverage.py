import numpy as np
import pytest
import xarray as xr

from lulucf import bgt_soilmap_coverage


@pytest.mark.unittest
def test_bgt_soilmap_coverage(bgt_gdf, simple_soilmap, lasso_grid):
    coverage = bgt_soilmap_coverage(bgt_gdf, simple_soilmap, lasso_grid)
    assert isinstance(coverage, xr.DataArray)
    assert coverage.dims == ("y", "x", "layer")
    assert coverage.sizes == {"y": 4, "x": 4, "layer": 36}
    assert np.isclose(coverage.sum(), 16)  # Sum in "layer" must be 1 for each "y", "x"
