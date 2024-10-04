from enum import StrEnum
from pathlib import Path, WindowsPath

import geopandas as gpd
from shapely.geometry import box

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

    _layers = SoilmapLayers

    @property
    def layers(self):
        return [f"{layer.value}" for layer in self._layers]

    def read_geometries(self):
        return gpd.read_file(self.file, layer=SoilmapLayers.SOILAREA)


def read_soilmap_geopackage(
    soilmap_path: str | WindowsPath, bbox: tuple = None
) -> gpd.GeoDataFrame:
    """
    Read and combine the required tables for LULUCF from the BRO soilmap into a single
    GeoDataFrame.

    The BRO Soilmap can be downloaded from PDOK with the following url:
    https://service.pdok.nl/bzk/bro-bodemkaart/atom/downloads/BRO_DownloadBodemkaart.gpkg

    Parameters
    ----------
    soilmap_path : str | WindowsPath
        Path to GeoPackage of the BRO Soilmap.
    bbox : tuple, optional
        Bounding box tuple (xmin, ymin, xmax, ymax) to return data for a selected area.

    Returns
    -------
    gpd.GeoDataFrame
        GeoDataFrame containing the relevant soilmap information.

    """
    with BroSoilmap(soilmap_path) as sm:
        soilmap = sm.read_geometries()
        soilunits = sm.read_table(SoilmapLayers.SOILAREA_SOILUNIT)

    soilmap = soilmap.merge(soilunits, on="maparea_id", how="left")

    if bbox:
        soilmap = soilmap.clip(box(*bbox))

    return soilmap
