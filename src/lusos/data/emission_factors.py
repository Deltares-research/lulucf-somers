from importlib import resources

import pandas as pd
import pooch

REGISTRY = pooch.create(
    path=pooch.os_cache("lusos"),
    base_url="https://github.com/Deltares-research/lulucf-somers/raw/main/data",
    version=None,
    env="LUSOS_DATA_DIR",
)
REGISTRY.load_registry(resources.files("lusos.data") / "registry.txt")


def ef_low_netherlands(year: int = 2023) -> pd.DataFrame:
    """
    Emission factors for the western part (low) part of the Netherlands for different BGT
    and soiltype combinations for different greenhouse gasses and flux directions (i.e.
    "out" or "in"). Fetches the data from a CSV file on the lulucf-somers repository.

    Parameters
    ----------
    year : int, optional
        Year of the emission factors to retrieve. The default is 2024.

    Returns
    -------
    pd.DataFrame
        Emission factors with index of BGT-soiltype combinations.

    """
    try:
        filename = REGISTRY.fetch(f"emission_factors_{year}_low_nl.csv")
        return pd.read_csv(filename, index_col="layer")
    except ValueError as e:
        raise ValueError(f"No emission factors available for year: {year}.") from e


def ef_high_netherlands(year: int = 2023) -> pd.DataFrame:
    """
    Emission factors for the eastern part (high) part of the Netherlands for different BGT
    and soiltype combinations for different greenhouse gasses and flux directions (i.e.
    "out" or "in"). Fetches the data from a CSV file on the lulucf-somers repository.

    Parameters
    ----------
    year : int, optional
        Year of the emission factors to retrieve. The default is 2024.

    Returns
    -------
    pd.DataFrame
        Emission factors with index of BGT-soiltype combinations.

    """
    try:
        filename = REGISTRY.fetch(f"emission_factors_{year}_high_nl.csv")
        return pd.read_csv(filename, index_col="layer")
    except ValueError as e:
        raise ValueError(f"No emission factors available for year: {year}.") from e
