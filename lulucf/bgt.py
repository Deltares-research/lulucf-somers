import pandas as pd
import geopandas as gpd
from pathlib import WindowsPath


BGT_LAYERS_FOR_LULUCF = [
    "pand_polygon",
    "wegdeel_polygon",
    "waterdeel_polygon",
    "ondersteunendwegdeel_polygon",
    "ondersteunendwaterdeel_polygon",
    "begroeidterreindeel_polygon",
    "onbegroeidterreindeel_polygon",
    "scheiding_polygon",
    "overigbouwwerk_polygon",
]


def combine_bgt_layers(bgt_gpkg: str | WindowsPath, layers: list) -> gpd.GeoDataFrame:
    """
    Combine layers from a BGT (Basisregistratie Grootschalige Topografie) geopackage into
    a single GeoDataFrame.

    Parameters
    ----------
    bgt_gpkg : str | WindowsPath
        Path to the geopackage (.gpkg file) to combine the layers from.
    layers : list
        Layers in the geopackage to combine.

    Returns
    -------
    gpd.GeoDataFrame
        GeoDataFrame of the combined layers.

    """
    combined = gpd.GeoDataFrame()
    for layer in layers:
        print(f"Read layer: {layer}")
        layer = gpd.read_file(bgt_gpkg, layer=layer)
        combined = pd.concat([combined, layer], ignore_index=True)
    return combined
