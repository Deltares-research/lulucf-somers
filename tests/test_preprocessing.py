import pytest
from numpy.testing import assert_array_equal

from lulucf.preprocessing import group_soilmap_units


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
