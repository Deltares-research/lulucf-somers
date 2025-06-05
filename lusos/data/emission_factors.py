from importlib import resources

import pandas as pd
import pooch

REGISTRY = pooch.create(
    path=pooch.os_cache("lusos"),
    base_url="https://github.com/Deltares-research/lusos/raw/main/data/",
    version=None,
    env="LUSOS_DATA_DIR",
)
REGISTRY.load_registry(resources.files("lusos.data") / "registry.txt")


def ef_low_netherlands():
    return pd.read_csv(
        REGISTRY.fetch("emission_factors.csv"),
        index_col="layer",
    )


def ef_high_netherlands():
    return pd.read_csv(
        REGISTRY.fetch("emission_factors_high_nl.csv"),
        index_col="layer",
    )
