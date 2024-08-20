from enum import StrEnum
from pathlib import Path, WindowsPath

import geopandas as gpd

from lulucf.readers import Geopackage


class SoilmapLayers(StrEnum):
    SOILAREA = "soilarea"
    AREAOFPEDOLOGICALINTEREST = "areaofpedologicalinterest"
    NGA_PROPERTIES = "nga_properties"
    SOILMAP = "soilmap"
    NORMALSOILPROFILES = "normalsoilprofiles"
    NORMALSOILPROFILES_LANDUSE = "normalsoilprofiles_landuse"
    SOILHORIZON = "soilhorizon"
    SOILHORIZON_FRACTIONPARTICLESIZE = "soilhorizon_fractionparticlesize"
    SOILLAYER = "soillayer"
    SOIL_UNITS = "soil_units"
    SOILCHARACTERISTICS_BOTTOMLAYER = "soilcharacteristics_bottomlayer"
    SOILCHARACTERISTICS_TOPLAYER = "soilcharacteristics_toplayer"
    SOILAREA_NORMALSOILPROFILE = "soilarea_normalsoilprofile"
    SOILAREA_SOILUNIT = "soilarea_soilunit"
    SOILAREA_SOILUNIT_SOILCHARACTERISTICSTOPLAYER = (
        "soilarea_soilunit_soilcharacteristicstoplayer"  # noqa: E501
    )
    SOILAREA_SOILUNIT_SOILCHARACTERISTICSBOTTOMLAYER = (
        "soilarea_soilunit_soilcharacteristicsbottomlayer"  # noqa: E501
    )


class BroSoilmap(Geopackage):
    """
    Class to handle to the BRO Soilmap geopackage. See lulucf.readers.Geopackage for
    available methods to query and inspect the tables in the geopackage.
    """

    def read_geometries(self):
        return gpd.read_file(self.file, layer=SoilmapLayers.SOILAREA)


def read_soilmap_geopackage(soilmap_path: str | WindowsPath) -> gpd.GeoDataFrame:
    """
    Read and combine the required tables for LULUCF from the BRO soilmap into a single
    GeoDataFrame.

    The BRO Soilmap can be downloaded from PDOK with the following url:
    https://service.pdok.nl/bzk/bro-bodemkaart/atom/downloads/BRO_DownloadBodemkaart.gpkg

    Parameters
    ----------
    soilmap_path : str | WindowsPath
        Path to GeoPackage of the BRO Soilmap.

    Returns
    -------
    gpd.GeoDataFrame
        GeoDataFrame containing the relevant soilmap information.

    """
    with BroSoilmap(soilmap_path) as sm:
        soilmap = sm.read_geometries()
        link_table = sm.read_table(SoilmapLayers.SOILAREA_NORMALSOILPROFILE)
        normalsoilprofile = sm.read_table(SoilmapLayers.NORMALSOILPROFILES)

    soilmap = soilmap.merge(link_table, on="maparea_id", how="left")
    soilmap = soilmap.merge(normalsoilprofile, on="normalsoilprofile_id", how="left")
    return soilmap
