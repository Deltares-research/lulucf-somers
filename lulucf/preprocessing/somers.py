import geopandas as gpd
import pandas as pd

from lulucf.validation import validate_somers


@validate_somers
def calc_somers_emission_per_m2(somers: gpd.GeoDataFrame) -> pd.Series:
    """
    Divide median emission factor (EF) by parcel area to calculate EF per ha. The input
    GeoDataFrame must have a column "median" present.

    Parameters
    ----------
    somers : gpd.GeoDataFrame
        Input SOMERS data with emission factors.

    Returns
    -------
    pd.Series
        Pandas Series with EF per ha.

    """
    return somers["median"] / somers["geometry"].area
