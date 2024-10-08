import itertools

import geopandas as gpd
import xarray as xr

from lulucf.area_statistics import areal_percentage_bgt_soilmap
from lulucf.constants import MAIN_BGT_UNITS, MAIN_SOILMAP_UNITS
from lulucf.lasso import LassoGrid
from lulucf.preprocessing import group_bgt_units, group_soilmap_units
from lulucf.utils import _add_layer_idx_column


def bgt_soilmap_coverage(
    bgt: gpd.GeoDataFrame, soilmap: gpd.GeoDataFrame, grid: LassoGrid
) -> xr.DataArray:
    """
    Calculate per cell in a grid for each combination of BGT and Soil Map polygons what
    percentage of a cell is covered by the combination. This returns a 3D DataArray with
    dimensions ('y', 'x', 'layer') where the dimension 'layer' contains ordered BGT-Soilmap
    layer combinations.

    Parameters
    ----------
    grid : lulucf.LassoGrid
        LassoGrid instance containing the raster grid to calculate the percentages for.
    bgt : gpd.GeoDataFrame
        GeoDataFrame containing the BGT data polygons.
    soilmap : gpd.GeoDataFrame
        GeoDataFrame containing the BGT data polygons.

    Returns
    -------
    xr.DataArray
        3D DataArray with the areal percentages.

    """
    bgt = _prepare_bgt(bgt, MAIN_BGT_UNITS)
    soilmap = _prepare_soilmap(soilmap, MAIN_SOILMAP_UNITS)

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


def _combine_bgt_soilmap_names(bgt_layers, soilmap_layers):
    return [f"{b}_{s}" for s, b in itertools.product(soilmap_layers, bgt_layers)]


def _prepare_bgt(bgt: gpd.GeoDataFrame, main_bgt_units: list):
    bgt = group_bgt_units(bgt)
    bgt = _add_layer_idx_column(bgt, main_bgt_units)
    return bgt


def _prepare_soilmap(soilmap: gpd.GeoDataFrame, main_soilmap_units: list):
    soilmap = group_soilmap_units(soilmap)
    soilmap = _add_layer_idx_column(soilmap, main_soilmap_units)
    soilmap.sort_values(by=["maparea_id", "soilunit_sequencenumber"], inplace=True)
    return soilmap.drop_duplicates(subset="maparea_id")
