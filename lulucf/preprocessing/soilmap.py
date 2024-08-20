from enum import StrEnum
from pathlib import Path, WindowsPath

import geopandas as gpd

from lulucf.readers import Geopackage

MAIN_SOILMAP_GROUPS = ["peat", "organic", "buried_peat", "non_organic"]


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
    def read_geometries(self):
        return gpd.read_file(self.file, layer=SoilmapLayers.SOILAREA)


def read_soilmap(soilmap_path: str | WindowsPath):
    with BroSoilmap(soilmap_path) as sm:
        soilmap = sm.read_geometries()
        link_table = sm.read_table(SoilmapLayers.SOILAREA_NORMALSOILPROFILE)
        normalsoilprofile = sm.read_table(SoilmapLayers.NORMALSOILPROFILES)

    soilmap = soilmap.merge(link_table, on="maparea_id", how="left")
    soilmap = soilmap.merge(normalsoilprofile, on='normalsoilprofile_id', how='left')
    return soilmap


workdir = Path(r"p:\11207812-somers-uitvoering\LULUCF_schil")
soilmap_gpkg = r"c:\Users\knaake\OneDrive - Stichting Deltares\Documents\data\dino\bro_bodemkaart.gpkg"
soilmap = read_soilmap(soilmap_gpkg)
