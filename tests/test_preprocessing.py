import pandas as pd
import pytest
from numpy.testing import assert_array_equal

from lulucf.preprocessing import calc_somers_emission_per_m2, group_soilmap_units


@pytest.mark.unittest
def test_group_soilmap_units(simple_soilmap):
    simple_soilmap = group_soilmap_units(simple_soilmap)

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
        "other",
    ]
    assert_array_equal(simple_soilmap["layer"], expected_result)


@pytest.mark.unittest
def test_calc_somers_emission_per_m2(somers_parcels):
    ef_per_ha = calc_somers_emission_per_m2(somers_parcels)
    assert isinstance(ef_per_ha, pd.Series)
