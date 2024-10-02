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


BGT_MAPPING = {
    "pand_": "openbare_ruimte",
    "wegdeel_rijbaan lokale weg": "openbare_ruimte",
    "wegdeel_inrit": "openbare_ruimte",
    "wegdeel_rijbaan regionale weg": "openbare_ruimte",
    "wegdeel_fietspad": "openbare_ruimte",
    "wegdeel_parkeervlak": "openbare_ruimte",
    "wegdeel_voetpad": "openbare_ruimte",
    "wegdeel_OV-baan": "openbare_ruimte",
    "wegdeel_voetgangersgebied": "openbare_ruimte",
    "wegdeel_voetpad op trap": "openbare_ruimte",
    "wegdeel_rijbaan autosnelweg": "openbare_ruimte",
    "wegdeel_rijbaan autoweg": "openbare_ruimte",
    "wegdeel_overweg": "openbare_ruimte",
    "wegdeel_spoorbaan": "openbare_ruimte",
    "wegdeel_woonerf": "openbare_ruimte",
    "wegdeel_ruiterpad": "openbare_ruimte",
    "waterdeel_waterloop": "sloten",
    "waterdeel_watervlakte": "grote_wateren",
    "waterdeel_greppel, droge sloot": "sloten",
    "waterdeel_zee": "grote_wateren",
    "ondersteunendwegdeel_berm": "stedelijk_groen",
    "ondersteunendwegdeel_verkeerseiland": "openbare_ruimte",
    "ondersteunendwaterdeel_oever, slootkant": "sloten",
    "ondersteunendwaterdeel_slik": "grote_wateren",
    "begroeidterreindeel_grasland agrarisch": "percelen",
    "begroeidterreindeel_grasland overig": "overig_groen",
    "begroeidterreindeel_groenvoorziening": "stedelijk_groen",
    "begroeidterreindeel_houtwal": "overig_groen",
    "begroeidterreindeel_duin": "overig_groen",
    "begroeidterreindeel_bouwland": "percelen",
    "begroeidterreindeel_struiken": "overig_groen",
    "begroeidterreindeel_loofbos": "overig_groen",
    "begroeidterreindeel_moeras": "overig_groen",
    "begroeidterreindeel_kwelder": "overig_groen",
    "begroeidterreindeel_fruitteelt": "overig_groen",
    "begroeidterreindeel_rietland": "overig_groen",
    "begroeidterreindeel_gemengd bos": "overig_groen",
    "begroeidterreindeel_boomteelt": "overig_groen",
    "begroeidterreindeel_naaldbos": "overig_groen",
    "begroeidterreindeel_heide": "overig_groen",
    "onbegroeidterreindeel_onverhard": "openbare_ruimte",
    "onbegroeidterreindeel_erf": "erven",
    "onbegroeidterreindeel_open verharding": "openbare_ruimte",
    "onbegroeidterreindeel_half verhard": "openbare_ruimte",
    "onbegroeidterreindeel_gesloten verharding": "openbare_ruimte",
    "onbegroeidterreindeel_zand": "openbare_ruimte",
    "scheiding_muur": "overig",
    "scheiding_kademuur": "overig",
    "overigbouwwerk_lage trafo": "overig",
    "overigbouwwerk_overkapping": "overig",
    "overigbouwwerk_open loods": "overig",
    "overigbouwwerk_niet-bgt": "overig",
    "overigbouwwerk_bassin": "overig",
    "overigbouwwerk_opslagtank": "overig",
    "overigbouwwerk_bezinkbak": "overig",
    "overigbouwwerk_windturbine": "overig",
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


def group_bgt_units(bgt: gpd.GeoDataFrame):
    bgt["bgt_type"] = bgt["bgt_type"].fillna("")
    combined_layers = bgt["layer"] + "_" + bgt["bgt_type"]

    for group in set(BGT_MAPPING.values()):
        units = [key for key in BGT_MAPPING.keys() if BGT_MAPPING[key] == group]
        bgt.loc[combined_layers.isin(units), "layer"] = group

    return bgt
