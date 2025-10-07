import geopandas as gpd

# Below ID's for main groups are based on SOMERS
PEAT_IDS = [
    "hVb",
    "hVs",
    "hVc",
    "hVr",
    "hVd",
    "hVk",
    "hVz",
    "hEV",
    "aVs",
    "aVc",
    "aVz",
    "aVp",
    "Vo",
    "pVb",
    "pVs",
    "pVc",
    "pVr",
    "pVd",
    "pVk",
    "pVz",
    "kVb",
    "kVs",
    "kVc",
    "kVr",
    "kVd",
    "kVk",
    "kVz",
    "zVs",
    "zVc",
    "zVz",
    "zVp",
    "Vb",
    "Vs",
    "Vc",
    "Vr",
    "Vd",
    "Vk",
    "Vz",
    "Vp",
    "iVs",
    "iVc",
    "iVz",
    "iVp",
    "AVo",
    "AP",
    "AAP",
]

MOER_IDS = [
    "kWp",
    "zWp",
    "vWp",
    "iWp",
    "kWz",
    "zWz",
    "uWz",
    "vWz",
    "iWz",
    "Wo",
    "Wg",
    "AWg",
    "AWv",
    "AVk",
    "ABv",
]

BURRIED_IDS = [
    "Rv01A",
    "Rv01C",
    "pRv81",
    "Mv51A",
    "Mv81A",
    "Mv41C",
    "Mv61C",
    "pMv51",
    "pMv81",
    "AEm9A",
    "AEm9",
    "AEm5",
    "AK",
    "ALu",
]

BURIED_DEEP_IDS = ["AEm8"]


def group_soilmap_units(soilmap: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Add a column to the soilmap GeoDataFrame containing main soil groups (i.e. "peat",
    "moerig", "buried" and "other") based on the ids of the soil units in the BRO soilmap.
    The main groups will be the "layer" dimension in the DataArray to calculate areal
    statistics with.

    Parameters
    ----------
    soilmap : gpd.GeoDataFrame
        GeoDataFrame containing the BRO soilmap and relevant information.

    Returns
    -------
    gpd.GeoDataFrame
        GeoDataFrame of the BRO soilmap with the added column.

    """
    soilmap["layer"] = "other"

    id_ = "soilunit_code"
    soilmap.loc[soilmap[id_].isin(PEAT_IDS), "layer"] = "peat"
    soilmap.loc[soilmap[id_].isin(MOER_IDS), "layer"] = "moerig"
    soilmap.loc[soilmap[id_].isin(BURRIED_IDS), "layer"] = "buried"
    soilmap.loc[soilmap[id_].isin(BURIED_DEEP_IDS), "layer"] = "buried_deep"

    return soilmap
