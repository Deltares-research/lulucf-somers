import warnings
from functools import wraps


def validate_somers(func):
    """
    Simple validation decorator to check GeoDataFrame with SOMERS input data.

    """

    @wraps(func)
    def wrapper(gdf):
        expected_columns = ["parcel_id", "median"]
        missing_columns = [c for c in expected_columns if c not in gdf.columns]
        if missing_columns:
            raise KeyError(f"SOMERS input missing columns: {missing_columns}")

        expected_crs = 28992
        if gdf.crs != expected_crs:
            warnings.warn(
                "crs of SOMERS input is not 'epsg:28992'. LULUCF calculations assume "
                "this crs in calculations with area. This may impact the results."
            )

        return func(gdf)

    return wrapper
