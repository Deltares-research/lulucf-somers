import geopandas as gpd

from lusos.area_statistics import calculate_model_flux
from lusos.lasso import LassoGrid
from lusos.preprocessing import calc_somers_emission_per_m2


def calculate_somers_emissions(
    somers: gpd.GeoDataFrame,
    grid: LassoGrid,
):
    """
    Calculate a weighted greenhouse gas flux per cell in a 2D grid from Somers emission
    data.

    Parameters
    ----------
    somers : gpd.GeoDataFrame
        _description_
    grid : LassoGrid
        _description_

    Returns
    -------
    _type_
        _description_
    """
    somers["flux_m2"] = calc_somers_emission_per_m2(somers)
    flux_per_m2 = calculate_model_flux(somers, grid)
    return flux_per_m2
