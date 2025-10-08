import pandas as pd
import pytest
from numpy.testing import assert_array_equal

from lusos import preprocessing as pr


@pytest.mark.unittest
def test_group_soilmap_units(simple_soilmap):
    simple_soilmap = pr.group_soilmap_units(simple_soilmap)

    expected_result = [
        "peat",
        "peat",
        "peat",
        "peat",
        "peat",
        "moerig",
        "moerig",
        "moerig",
        "moerig",
        "buried",
        "buried",
        "buried",
        "buried",
    ]
    assert_array_equal(simple_soilmap["layer"], expected_result)


@pytest.mark.unittest
def test_calc_somers_emission_per_m2(somers_parcels):
    ef_per_ha = pr.calc_somers_emission_per_m2(somers_parcels)
    assert isinstance(ef_per_ha, pd.Series)


@pytest.mark.unittest
def test_group_bgt_units(bgt_gdf):
    bgt_gdf = pr.group_bgt_units(bgt_gdf)
    expected_groups = [
        "percelen",
        "openbare_ruimte",
        "stedelijk_groen",
        "openbare_ruimte",
        "sloten",
        "panden",
        "percelen",
        "overig_groen",
        "sloten",
        "stedelijk_groen",
        "percelen",
        "overig",
        "overig_groen",
        "overig",
    ]
    assert_array_equal(bgt_gdf["layer"], expected_groups)
