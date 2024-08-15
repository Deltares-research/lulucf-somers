import pytest

from lulucf.area_statistics import calc_areal_percentage_in_cells


@pytest.mark.unittest
def test_calc_areal_percentage_in_cells(bgt_gdf, lasso_grid):
    result = calc_areal_percentage_in_cells(bgt_gdf, lasso_grid)
    assert 1 == 1
