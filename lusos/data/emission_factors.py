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
    filename = REGISTRY.fetch("emission_factors_low_nl.csv")
    return pd.read_csv(filename, index_col="layer")


def ef_high_netherlands():
    filename = REGISTRY.fetch("emission_factors_high_nl.csv")
    return pd.read_csv(filename, index_col="layer")
