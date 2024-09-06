import itertools

import geopandas as gpd
import numpy as np
import xarray as xr

from lulucf.area_statistics import calc_flux_and_coverage_for
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


@profile_function
def calculate_emissions(
    somers: gpd.GeoDataFrame,
    grid: LassoGrid,
    soilmap: gpd.GeoDataFrame,
    bgt: gpd.GeoDataFrame,
    use_dask: bool = True,
):
    somers_mask = rasterize_as_mask(somers, grid.dataarray(), invert=True)
    valid_idx = get_valid_indices(somers_mask)

    soilmap = group_soilmap_units(soilmap)

    layers_areal = _combine_bgt_soilmap_names(MAIN_BGT_UNITS, MAIN_SOILMAP_UNITS)
    areal = grid.empty_array(layers_areal, use_dask)

    bgt = _add_layer_idx_column(bgt, MAIN_BGT_UNITS)
    soilmap = _add_layer_idx_column(soilmap, MAIN_SOILMAP_UNITS)

    flux_per_ha = grid.dataarray(np.nan)

    flux_per_ha, areal = calc_flux_and_coverage_for(
        valid_idx, somers, bgt, soilmap, flux_per_ha, areal
    )

    return flux_per_ha, areal
