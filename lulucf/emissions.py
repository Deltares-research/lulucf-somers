import itertools

import geopandas as gpd
import numpy as np
import xarray as xr

from lulucf.area_statistics import areal_percentage_bgt_soilmap
from lulucf.lasso import LassoGrid
from lulucf.preprocessing import group_soilmap_units
from lulucf.utils import (
    _add_layer_idx_column,
    get_valid_indices,
    profile_function,
    rasterize_as_mask,
)

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


# @profile_function
def calculate_emissions(
    somers: gpd.GeoDataFrame,
    grid: LassoGrid,
    soilmap: gpd.GeoDataFrame,
    bgt: gpd.GeoDataFrame,
    use_dask: bool = True,
):
    soilmap = group_soilmap_units(soilmap)

    bgt = _add_layer_idx_column(bgt, MAIN_BGT_UNITS)
    soilmap = _add_layer_idx_column(soilmap, MAIN_SOILMAP_UNITS)

    flux_per_ha = grid.dataarray(np.nan)

    area = areal_percentage_bgt_soilmap(
        grid, bgt, soilmap, MAIN_BGT_UNITS, MAIN_SOILMAP_UNITS, use_dask
    )
    layers_area = _combine_bgt_soilmap_names(MAIN_BGT_UNITS, MAIN_SOILMAP_UNITS)
    xco = grid.xcoordinates()
    yco = grid.ycoordinates()

    area = xr.DataArray(
        area.reshape(len(yco), len(xco), len(layers_area)),
        coords={"y": yco, "x": xco, "layer": layers_area},
        dims=("y", "x", "layer"),
    )

    return
