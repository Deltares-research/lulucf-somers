import itertools

import geopandas as gpd
import numpy as np
import xarray as xr

from lulucf.area_statistics import areal_percentage_bgt_soilmap, calculate_somers_flux
from lulucf.lasso import LassoGrid
from lulucf.preprocessing import calc_somers_emission_per_m2, group_soilmap_units
from lulucf.utils import _add_layer_idx_column

MAIN_SOILMAP_UNITS = ["peat", "moerig", "buried", "other"]
MAIN_BGT_UNITS = [
    "pand",
    "wegdeel",
    "waterdeel",
    "ondersteunendwegdeel",
    "ondersteunendwaterdeel",
    "begroeidterreindeel",
    "onbegroeidterreindeel",
    "scheiding",
    "overigbouwwerk",
]


def _combine_bgt_soilmap_names(bgt_layers, soilmap_layers):
    return [f"{b}_{s}" for s, b in itertools.product(soilmap_layers, bgt_layers)]


def calculate_emissions(
    somers: gpd.GeoDataFrame,
    grid: LassoGrid,
    soilmap: gpd.GeoDataFrame,
    bgt: gpd.GeoDataFrame,
):
    somers['median_m2'] = calc_somers_emission_per_m2(somers)
    flux_per_m2 = calculate_somers_flux(somers, grid)

    area = bgt_soilmap_coverage_grid(bgt, soilmap, grid)

    return flux_per_m2, area


def bgt_soilmap_coverage_grid(bgt, soilmap, grid):
    soilmap = group_soilmap_units(soilmap)

    bgt = _add_layer_idx_column(bgt, MAIN_BGT_UNITS)
    soilmap = _add_layer_idx_column(soilmap, MAIN_SOILMAP_UNITS)

    area = areal_percentage_bgt_soilmap(
        grid, bgt, soilmap, MAIN_BGT_UNITS, MAIN_SOILMAP_UNITS
    )
    layers_area = _combine_bgt_soilmap_names(MAIN_BGT_UNITS, MAIN_SOILMAP_UNITS)
    xco = grid.xcoordinates()
    yco = grid.ycoordinates()

    area = xr.DataArray(
        area.reshape(len(yco), len(xco), len(layers_area)),
        coords={"y": yco, "x": xco, "layer": layers_area},
        dims=("y", "x", "layer"),
    )
    return area
