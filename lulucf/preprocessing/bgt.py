from pathlib import WindowsPath

import geopandas as gpd
import pandas as pd

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


def _read_layers(bgt_gpkg: str | WindowsPath, layers: list):
    """
    Helper function for combine_bgt_layers to read the BGT layers and add the required
    information for LULUCF. Returns a generator with GeoDataFrames for each layer.

    """
    for layer in layers:
        print(f"Read layer: {layer}")
        layer_gdf = gpd.read_file(bgt_gpkg, layer=layer, columns="geometry")
        layer_gdf["layer"] = layer.replace("_polygon", "")
        yield layer_gdf


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
    combined = pd.concat(_read_layers(bgt_gpkg, layers), ignore_index=True)
    return combined
