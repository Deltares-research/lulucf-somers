import numpy as np
import pytest
from numpy.testing import assert_approx_equal, assert_array_almost_equal

from lulucf.area_statistics import (
    _calc_coverage_percentage,
    calc_areal_percentage_in_cells,
    calc_flux_and_coverage_for,
    somers_flux_in,
)
from lulucf.emissions import (
    MAIN_BGT_UNITS,
    MAIN_SOILMAP_UNITS,
    _combine_bgt_soilmap_names,
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
    simple_soilmap["layer"] = np.repeat(
        ["peat", "moerig", "buried", "other"], [5, 4, 4, 1]
    )
    simple_soilmap["idx"] = np.repeat([0, 1, 2, 3], [5, 4, 4, 1])
    return simple_soilmap


@pytest.fixture
def empty_areal_array(lasso_grid):
    layers = _combine_bgt_soilmap_names(MAIN_BGT_UNITS, MAIN_SOILMAP_UNITS)
    return lasso_grid.empty_array(layers, dask=False)


@pytest.mark.unittest
def test_calc_areal_percentage_in_cells(bgt_gdf, empty_bgt_array):
    bgt_gdf = _add_layer_idx_column(bgt_gdf, MAIN_BGT_UNITS)

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
def test_calc_flux_and_coverage_for(
    lasso_grid, bgt_gdf, somers_parcels, grouped_soilmap, empty_areal_array
):
    bgt_gdf = _add_layer_idx_column(bgt_gdf, MAIN_BGT_UNITS)
    flux = lasso_grid.dataarray(np.nan)
    test_indices = [[1, 2], [2, 1]]
    flux, areal = calc_flux_and_coverage_for(
        test_indices, somers_parcels, bgt_gdf, grouped_soilmap, flux, empty_areal_array
    )

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
def test_calc_coverage_percentage(raster_cell, grouped_soilmap):
    ngroups = 4
    cellarea = 1
    perc = _calc_coverage_percentage(raster_cell, grouped_soilmap, cellarea, ngroups)
    expected_result = [0, 0.84455372, 0.03044628, 0.125]
    assert_array_almost_equal(perc, expected_result)


@pytest.mark.unittest
def test_somers_flux_in(raster_cell, somers_parcels):
    flux = somers_flux_in(raster_cell, somers_parcels)
    assert_approx_equal(flux, 4801.43383)
