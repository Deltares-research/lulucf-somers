from pathlib import Path

import geopandas as gpd

# Below ID's for main groups are based on SOMERS
PEAT_IDS = [
    1010,
    1030,
    1050,
    1050,
    1050,
    1060,
    1070,
    1050,
    1080,
    1080,
    1100,
    1120,
    1281,
    1130,
    1150,
    1170,
    1170,
    1170,
    1240,
    1180,
    1190,
    1200,
    1220,
    1220,
    1220,
    1240,
    1230,
    1260,
    1260,
    1250,
    1270,
    1290,
    1281,
    1290,
    1290,
    1290,
    1300,
    1310,
    1320,
    1330,
    1330,
    1340,
    1350,
    1320,
    1281,
    1250,
]

MOER_IDS = [
    2010,
    2040,
    2020,
    2060,
    2110,
    2120,
    2125,
    2130,
    2160,
    2080,
    2081,
    2081,
    15020,
    15100,
    2110,
]

BURRIED_IDS = [
    16040,
    16040,
    16010,
    15100,
    15110,
    15130,
    15120,
    15010,
    15020,
    15340,
    15441,
    15441,
    15402,
    15120,
    15441,
]


def group_soilmap_units(soilmap: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Add a column to the soilmap GeoDataFrame containing main soil groups (i.e. "peat",
    "moerig", "buried" and "other") based on the ids of the soil units in the BRO soilmap.

    Parameters
    ----------
    soilmap : gpd.GeoDataFrame
        GeoDataFrame containing the BRO soilmap and relevant information.

    Returns
    -------
    gpd.GeoDataFrame
        GeoDataFrame of the BRO soilmap with the added column.

    """
    soilmap["main_group"] = "other"

    id_ = "normalsoilprofile_id"
    soilmap.loc[soilmap[id_].isin(PEAT_IDS), "main_group"] = "peat"
    soilmap.loc[soilmap[id_].isin(MOER_IDS), "main_group"] = "moerig"
    soilmap.loc[soilmap[id_].isin(BURRIED_IDS), "main_group"] = "buried"

    return soilmap
