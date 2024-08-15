import geopandas as gpd

from lulucf.lasso import LassoGrid


def calc_areal_percentage_in_cells(bgt_data: gpd.GeoDataFrame, grid: LassoGrid):
    cells = grid.lasso_cells_as_geometries()
    return
