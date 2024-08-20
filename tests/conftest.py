import itertools

import geopandas as gpd
import numpy as np
import pandas as pd
import pytest
from scipy.spatial import Voronoi
from shapely.geometry import LineString, MultiPolygon, box
from shapely.ops import polygonize

from lulucf.lasso import LassoGrid
from lulucf.preprocessing.bgt import BGT_LAYERS_FOR_LULUCF
from lulucf.readers import read_soilmap_geopackage


def create_polygons():
    points = [
        [0, 0],
        [0, 4],
        [4, 4],
        [4, 0],
        [0.5, 0.5],
        [0.7, 3],
        [1, 1.5],
        [2.1, 2.3],
        [2.7, 0.8],
        [3.1, 3.1],
        [3.3, 1.9],
        [1.8, 3.5],
        [1.5, 0.8],
        [1.4, 1.0],
    ]

    vor = Voronoi(points)

    lines = [
        LineString(vor.vertices[line]) for line in vor.ridge_vertices if -1 not in line
    ]
    polygons = MultiPolygon(polygonize(lines))
    bbox = box(0, 0, 4, 4)

    corners = bbox.difference(polygons)
    polygons = [geom.intersection(bbox) for geom in polygons.geoms]
    return [*polygons, *corners.geoms]


@pytest.fixture
def lasso_grid() -> LassoGrid:
    """
    LassoGrid instance with simple bounds.

    """
    xmin, xmax = 0, 4
    ymin, ymax = 0, 4
    cellsize = 1
    return LassoGrid(xmin, ymin, xmax, ymax, cellsize, cellsize)


@pytest.fixture
def raster_file(lasso_grid, tmp_path):
    """
    Temporary raster file from the lasso_grid fixture.

    """
    outfile = tmp_path / r"temp.tif"
    da = lasso_grid.dataarray()
    da.rio.to_raster(outfile)
    return outfile


@pytest.fixture
def bgt_gdf():
    """
    GeoDataFrame containing simple polygons in the area of the lasso_grid fixture to test
    operations involving BGT data.

    """
    polygons = create_polygons()

    layers = []
    bgt_cycle = itertools.cycle(BGT_LAYERS_FOR_LULUCF)
    for ii, layer in enumerate(bgt_cycle):
        if ii == len(polygons):
            break
        layers.append(layer.replace("_polygon", ""))

    bgt_data = {"layer": layers, "geometry": polygons}
    return gpd.GeoDataFrame(bgt_data)


@pytest.fixture
def empty_bgt_array(lasso_grid):
    bgt_layers = [layer.replace("_polygon", "") for layer in BGT_LAYERS_FOR_LULUCF]
    return lasso_grid.empty_array(bgt_layers, dask=False)


@pytest.fixture
def simple_soilmap_path(tmp_path):
    """
    Fixture to create a tmp geopackage file that contains relevant BRO soilmap information
    to test.

    """
    polygons = create_polygons()
    maparea_id = np.arange(len(polygons))
    normalsoilprofile_id = [
        1170,
        1240,
        1060,
        1070,
        1050,
        2020,
        2060,
        2110,
        2120,
        16040,
        16010,
        15100,
        15110,
        1225,
    ]
    soilunits = [
        "pVc",
        "pVk",
        "hVk",
        "hVz",
        "hEV",
        "vWp",
        "iWp",
        "kWz",
        "zWz",
        "Rv01C",
        "pRv81",
        "Mv51A",
        "Mv81A",
        "kVc",
    ]
    geometries = gpd.GeoDataFrame({"maparea_id": maparea_id, "geometry": polygons})
    link_table = gpd.GeoDataFrame(
        {"maparea_id": maparea_id, "normalsoilprofile_id": normalsoilprofile_id}
    )
    normalsoilprofile = gpd.GeoDataFrame(
        {"normalsoilprofile_id": normalsoilprofile_id, "soilunit": soilunits}
    )

    layers = ["soilarea", "soilarea_normalsoilprofile", "normalsoilprofiles"]
    tables = [geometries, link_table, normalsoilprofile]

    outfile = tmp_path / "soilmap.gpkg"
    for layer, table in zip(layers, tables):
        table.to_file(outfile, driver="GPKG", layer=layer, index=False)

    return outfile


@pytest.fixture
def simple_soilmap(simple_soilmap_path):
    return read_soilmap_geopackage(simple_soilmap_path)
