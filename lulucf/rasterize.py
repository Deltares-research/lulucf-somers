import numpy as np
import geopandas as gpd
import xarray as xr
from pathlib import WindowsPath
from rasterio import features


def rasterize_like(
    shapefile: str | WindowsPath | gpd.GeoDataFrame,
    attribute: str,
    da: xr.DataArray,
):
    """
    Rasterize a shapefile like an atmod Raster or into the 2D extent of a VoxelModel
    object.

    Parameters
    ----------
    shapefile : str | WindowsPath | gpd.GeoDataFrame
        Input shapefile to rasterize. Can be a path to the shapefile or an in
        memory GeoDataFrame.
    attribute : str
        Name of the attribute in the shapefile to rasterize.
    da : xr.DataArray,
        Atmod Raster or VoxelModel object to rasterize the shapefile like.
    cellsize : int, optional
        Cellsize of the output DataArray. The default is None, then the x and y
        size will be derived from the input DataArray.

    Returns
    -------
    xr.DataArray
        DataArray of the rasterized shapefile.

    """
    if isinstance(shapefile, (str, WindowsPath)):
        shapefile = gpd.read_file(shapefile)

    shapes = ((geom, z) for z, geom in zip(shapefile[attribute], shapefile["geometry"]))

    rasterized = features.rasterize(
        shapes=shapes,
        fill=np.nan,
        out_shape=(da.nrows, da.ncols),
        transform=da.get_affine(),
    )
    rasterized = xr.DataArray(rasterized, coords=da.coords, dims=da.dims)
    return rasterized
