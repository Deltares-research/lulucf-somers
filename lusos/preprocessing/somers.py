import geopandas as gpd
import pandas as pd

from lusos.validation import validate_somers


@validate_somers
def calc_somers_emission_per_m2(somers: gpd.GeoDataFrame) -> pd.Series:
    """
    Divide median emission factor (EF; ton/ha) by parcel area to calculate EF per m2.
    The input GeoDataFrame must have a column "median" present.

    Parameters
    ----------
    somers : gpd.GeoDataFrame
        Input SOMERS data with emission factors in ton/ha.

    Returns
    -------
    pd.Series
        Pandas Series with EF per m2.

    """
    to_m2 = 10_000
    return somers["median"] / to_m2
