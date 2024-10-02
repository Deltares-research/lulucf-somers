from pathlib import WindowsPath

import geopandas as gpd
import pandas as pd

BGT_LAYERS_FOR_LULUCF = {
    "pand_polygon": "bgt_functie",
    "wegdeel_polygon": "bgt_functie",
    "waterdeel_polygon": "bgt_type",
    "ondersteunendwegdeel_polygon": "bgt_functie",
    "ondersteunendwaterdeel_polygon": "bgt_type",
    "begroeidterreindeel_polygon": "bgt_fysiekvoorkomen",
    "onbegroeidterreindeel_polygon": "bgt_fysiekvoorkomen",
    "scheiding_polygon": "bgt_type",
    "overigbouwwerk_polygon": "bgt_type",
}


def _read_layers(bgt_gpkg: str | WindowsPath, layers: dict):
    """
    Helper function for combine_bgt_layers to read the BGT layers and add the required
    information for LULUCF. Returns a generator with GeoDataFrames for each layer.

    """
    for layer in layers.keys():
        print(f"Read layer: {layer}")
        layer_gdf = gpd.read_file(
            bgt_gpkg, layer=layer, columns=[layers[layer], "geometry"]
        )
        layer_gdf.rename(columns={layers[layer]: "bgt_type"}, inplace=True)
        layer_gdf["layer"] = layer.replace("_polygon", "")
        yield layer_gdf


def combine_bgt_layers(
    bgt_gpkg: str | WindowsPath, layers: dict = BGT_LAYERS_FOR_LULUCF
) -> gpd.GeoDataFrame:
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
