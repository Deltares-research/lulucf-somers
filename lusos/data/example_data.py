from importlib import resources

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


def sample_bgt():
    """
    Sample BGT data for the Netherlands. Fetches the data from a geoparquet file on the
    lulucf-somers repository.

    Returns
    -------
    gpd.GeoDataFrame
        Sample BGT data with geometry and attributes.

    """
    filename = REGISTRY.fetch("bgt_data.geoparquet")
    return gpd.read_parquet(filename)


def sample_soilmap():
    """
    Sample soil map data for the Netherlands. Fetches the data from a GeoPackage file on
    the lulucf-somers repository.

    Returns
    -------
    gpd.GeoDataFrame
        Sample soil map data with geometry and attributes.

    """
    filename = REGISTRY.fetch("bro_soilmap.gpkg")
    return read_soilmap_geopackage(filename)


def sample_emissions():
    """
    Sample emissions data for the Netherlands. Fetches the data from a geoparquet file on
    the lulucf-somers repository.

    Returns
    -------
    gpd.GeoDataFrame
        Sample emissions data with geometry and attributes.

    """
    filename = REGISTRY.fetch("emissions.geoparquet")
    return gpd.read_parquet(filename)
