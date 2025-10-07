from importlib import resources
from pathlib import Path

import geopandas as gpd
import pooch

from lusos.readers import read_soilmap_geopackage

REGISTRY = pooch.create(
    path=pooch.os_cache("lusos"),
    base_url="https://github.com/Deltares-research/lulucf-somers/raw/main/data",
    version=None,
    env="LUSOS_DATA_DIR",
)
REGISTRY.load_registry(resources.files("lusos.data") / "registry.txt")


def sample_bgt(as_path: bool = False):
    """
    Sample BGT data for the Netherlands. Fetches the data from a geoparquet file on the
    lulucf-somers repository.

    Returns
    -------
    gpd.GeoDataFrame
        Sample BGT data with geometry and attributes.

    """
    filename = REGISTRY.fetch("bgt_data.geoparquet")
    if as_path:
        return Path(filename)
    else:
        return gpd.read_parquet(filename)


def sample_soilmap(as_path: bool = False):
    """
    Sample soil map data for the Netherlands. Fetches the data from a GeoPackage file on
    the lulucf-somers repository.

    Returns
    -------
    gpd.GeoDataFrame
        Sample soil map data with geometry and attributes.

    """
    filename = REGISTRY.fetch("bro_soilmap.gpkg")
    if as_path:
        return Path(filename)
    else:
        return read_soilmap_geopackage(filename)


def sample_emissions(as_path: bool = False):
    """
    Sample emissions data for the Netherlands. Fetches the data from a geoparquet file on
    the lulucf-somers repository.

    Returns
    -------
    gpd.GeoDataFrame
        Sample emissions data with geometry and attributes.

    """
    filename = REGISTRY.fetch("emissions.geoparquet")
    if as_path:
        return Path(filename)
    else:
        return gpd.read_parquet(filename)
