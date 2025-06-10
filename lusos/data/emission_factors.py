from importlib import resources

import pandas as pd
import pooch

REGISTRY = pooch.create(
    path=pooch.os_cache("lusos"),
    base_url="https://github.com/Deltares-research/lulucf-somers/raw/feature/pooch/data",
    version=None,
    env="LUSOS_DATA_DIR",
)
REGISTRY.load_registry(resources.files("lusos.data") / "registry.txt")


def ef_low_netherlands():
    """
    Emission factors for the western part (low) part of the Netherlands for different BGT
    and soiltype combinations for different greenhouse gasses and flux directions (i.e. "out"
    or "in"). Fetches the data from a CSV file on the lulucf-somers repository.

    Returns
    -------
    pd.DataFrame
        Emission factors with index of BGT-soiltype combinations.

    """
    filename = REGISTRY.fetch("emission_factors_low_nl.csv")
    return pd.read_csv(filename, index_col="layer")


def ef_high_netherlands():
    """
    Emission factors for the eastern part (high) part of the Netherlands for different BGT
    and soiltype combinations for different greenhouse gasses and flux directions (i.e. "out"
    or "in"). Fetches the data from a CSV file on the lulucf-somers repository.

    Returns
    -------
    pd.DataFrame
        Emission factors with index of BGT-soiltype combinations.

    """
    filename = REGISTRY.fetch("emission_factors_high_nl.csv")
    return pd.read_csv(filename, index_col="layer")
