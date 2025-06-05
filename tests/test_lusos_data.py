import pandas as pd
import pytest

import lusos


def expected_ef_low_netherlands():
    return pd.DataFrame(
        [
            ["panden_peat", 1.025, 0, 0, 0],
            ["overig_groen_peat", 1.025, 0, 0, 0],
            ["percelen_peat", 1.025, 0, 0, 0],
            ["openbare_ruimte_peat", 1.025, 0, 0, 0],
            ["grote_wateren_peat", 0, 0, 0, 0],
            ["erven_peat", 1.025, 0, 0, 0],
            ["overig_peat", 1.025, 0, 0, 0],
            ["sloten_peat", 0, 0.0518, 0, 0],
            ["stedelijk_groen_peat", 1.025, 0, 0, 0],
            ["panden_moerig", 1.236, 0, 0, 0],
            ["overig_groen_moerig", 1.236, 0, 0, 0],
            ["percelen_moerig", 1.236, 0, 0, 0],
            ["openbare_ruimte_moerig", 1.236, 0, 0, 0],
            ["grote_wateren_moerig", 0, 0, 0, 0],
            ["erven_moerig", 1.236, 0, 0, 0],
            ["overig_moerig", 1.236, 0, 0, 0],
            ["sloten_moerig", 0, 0, 0, 0],
            ["stedelijk_groen_moerig", 1.236, 0, 0, 0],
            ["panden_buried", 0, 0, 0, 0],
            ["overig_groen_buried", 0, 0, 0, 0],
            ["percelen_buried", 0, 0, 0, 0],
            ["openbare_ruimte_buried", 0, 0, 0, 0],
            ["grote_wateren_buried", 0, 0, 0, 0],
            ["erven_buried", 0, 0, 0, 0],
            ["overig_buried", 0, 0, 0, 0],
            ["sloten_buried", 0, 0, 0, 0],
            ["stedelijk_groen_buried", 0, 0, 0, 0],
            ["panden_other", 0, 0, 0, 0],
            ["overig_groen_other", 0, 0, 0, 0],
            ["percelen_other", 0, 0, 0, 0],
            ["openbare_ruimte_other", 0, 0, 0, 0],
            ["grote_wateren_other", 0, 0, 0, 0],
            ["erven_other", 0, 0, 0, 0],
            ["overig_other", 0, 0, 0, 0],
            ["sloten_other", 0, 0, 0, 0],
            ["stedelijk_groen_other", 0, 0, 0, 0],
        ],
        columns=["layer", "co2_uit", "ch4_uit", "n2o_uit", "co2_in"],
    ).set_index("layer")


def expected_ef_high_netherlands():
    pd.DataFrame(
        [
            ["panden_peat", 2.570, 0.000, 0.000, 0.000],
            ["overig_groen_peat", 2.570, 0.000, 0.000, 0.000],
            ["percelen_peat", 2.570, 0.000, 0.000, 0.000],
            ["openbare_ruimte_peat", 2.570, 0.000, 0.000, 0.000],
            ["grote_wateren_peat", 0.000, 0.000, 0.000, 0.000],
            ["erven_peat", 2.570, 0.000, 0.000, 0.000],
            ["overig_peat", 2.570, 0.000, 0.000, 0.000],
            ["sloten_peat", 0.000, 0.052, 0.000, 0.000],
            ["stedelijk_groen_peat", 2.570, 0.000, 0.000, 0.000],
            ["panden_moerig", 1.300, 0.000, 0.000, 0.000],
            ["overig_groen_moerig", 1.300, 0.000, 0.000, 0.000],
            ["percelen_moerig", 1.300, 0.000, 0.000, 0.000],
            ["openbare_ruimte_moerig", 1.300, 0.000, 0.000, 0.000],
            ["grote_wateren_moerig", 0.000, 0.000, 0.000, 0.000],
            ["erven_moerig", 1.300, 0.000, 0.000, 0.000],
            ["overig_moerig", 1.300, 0.000, 0.000, 0.000],
            ["sloten_moerig", 0.000, 0.000, 0.000, 0.000],
            ["stedelijk_groen_moerig", 1.300, 0.000, 0.000, 0.000],
            ["panden_buried", 0.000, 0.000, 0.000, 0.000],
            ["overig_groen_buried", 0.000, 0.000, 0.000, 0.000],
            ["percelen_buried", 0.000, 0.000, 0.000, 0.000],
            ["openbare_ruimte_buried", 0.000, 0.000, 0.000, 0.000],
            ["grote_wateren_buried", 0.000, 0.000, 0.000, 0.000],
            ["erven_buried", 0.000, 0.000, 0.000, 0.000],
            ["overig_buried", 0.000, 0.000, 0.000, 0.000],
            ["sloten_buried", 0.000, 0.000, 0.000, 0.000],
            ["stedelijk_groen_buried", 0.000, 0.000, 0.000, 0.000],
            ["panden_other", 0.000, 0.000, 0.000, 0.000],
            ["overig_groen_other", 0.000, 0.000, 0.000, 0.000],
            ["percelen_other", 0.000, 0.000, 0.000, 0.000],
            ["openbare_ruimte_other", 0.000, 0.000, 0.000, 0.000],
            ["grote_wateren_other", 0.000, 0.000, 0.000, 0.000],
            ["erven_other", 0.000, 0.000, 0.000, 0.000],
            ["overig_other", 0.000, 0.000, 0.000, 0.000],
            ["sloten_other", 0.000, 0.000, 0.000, 0.000],
            ["stedelijk_groen_other", 0.000, 0.000, 0.000, 0.000],
        ],
        columns=["layer", "co2_uit", "ch4_uit", "n2o_uit", "co2_in"],
    ).set_index("layer")


@pytest.mark.unittest
def test_low_nl():
    ef = lusos.data.ef_low_netherlands()
    assert isinstance(ef, pd.DataFrame)
    assert ef.equals(expected_ef_low_netherlands())


@pytest.mark.unittest
def test_high_nl():
    ef = lusos.data.ef_high_netherlands()
    assert isinstance(ef, pd.DataFrame)
    assert ef.equals(expected_ef_high_netherlands())
