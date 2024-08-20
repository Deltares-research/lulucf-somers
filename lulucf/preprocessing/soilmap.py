from enum import StrEnum
from pathlib import Path, WindowsPath

import geopandas as gpd

from lulucf.readers import read_soilmap_geopackage

MAIN_SOILMAP_GROUPS = ["peat", "organic", "buried_peat", "non_organic"]


workdir = Path(r"p:\11207812-somers-uitvoering\LULUCF_schil")
soilmap_gpkg = r"c:\Users\knaake\OneDrive - Stichting Deltares\Documents\data\dino\bro_bodemkaart.gpkg"
soilmap = read_soilmap_geopackage(soilmap_gpkg)
