import geopandas as gpd
import numpy as np
import pandas as pd
import xarray as xr

from lulucf.utils import cell_as_geometry


def _add_layer_idx_column(gdf: gpd.GeoDataFrame, da: xr.DataArray):
    df = pd.DataFrame(da["layer"].values, columns=["layer"])
    df.index.name = "idx"
    df.reset_index(inplace=True)
    gdf = gdf.merge(df, on="layer", how="left")
    return gdf


def calculate_areal_percentages_bgt(bgt_data: gpd.GeoDataFrame, da: xr.DataArray):
    bgt_data = _add_layer_idx_column(bgt_data, da)
    da = calc_areal_percentage_in_cells(bgt_data, da)
    return da


def calc_areal_percentage_in_cells(polygons: gpd.GeoDataFrame, da: xr.DataArray):
    if "idx" not in polygons.columns:
        raise KeyError("GeoDataFrame must contain an 'idx' column.")

    if "y" not in da.dims or "x" not in da.dims:
        raise KeyError("DataArray must contain dimensions 'y' and 'x'.")

    cellsize = da.rio.resolution()
    cellarea = np.abs((cellsize[0] * cellsize[1]) ** 2)

    for i, y in enumerate(da["y"]):
        for j, x in enumerate(da["x"]):
            geom = cell_as_geometry(x, y, cellsize)

            cell_clip = polygons.clip(geom)

            percentage = cell_clip["geometry"].area / cellarea
            idx = cell_clip["idx"].values

            da[i, j, idx] = percentage.values

    return da
