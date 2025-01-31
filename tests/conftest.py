import itertools

import geopandas as gpd
import numpy as np
import pandas as pd
import pytest
from scipy.spatial import Voronoi
from shapely.geometry import LineString, MultiPolygon, box
from shapely.ops import polygonize

from lusos.lasso import LassoGrid
from lusos.preprocessing.bgt import BGT_LAYERS_FOR_LUSOS
from lusos.readers import read_soilmap_geopackage


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

    layers = [
        "begroeidterreindeel",
        "onbegroeidterreindeel",
        "begroeidterreindeel",
        "wegdeel",
        "waterdeel",
        "pand",
        "begroeidterreindeel",
        "begroeidterreindeel",
        "ondersteunendwaterdeel",
        "ondersteunendwegdeel",
        "begroeidterreindeel",
        "scheiding",
        "begroeidterreindeel",
        "overigbouwwerk",
    ]

    bgt_type = [
        "grasland agrarisch",
        "half verhard",
        "groenvoorziening",
        "rijbaan regionale weg",
        "waterloop",
        "",
        "grasland agrarisch",
        "loofbos",
        "oever, slootkant",
        "berm",
        "bouwland",
        "kademuur",
        "rietland",
        "open loods",
    ]

    bgt_data = {"layer": layers, "bgt_type": bgt_type, "geometry": polygons}
    return gpd.GeoDataFrame(bgt_data, crs=28992)


@pytest.fixture
def empty_bgt_array(lasso_grid):
    bgt_layers = [layer.replace("_polygon", "") for layer in BGT_LAYERS_FOR_LUSOS]
    return lasso_grid.empty_array(bgt_layers, dask=False)


@pytest.fixture
def empty_soilmap_array(lasso_grid):
    layers = ["peat", "moerig", "buried", "other"]
    return lasso_grid.empty_array(layers, dask=False)


@pytest.fixture
def simple_soilmap_path(tmp_path):
    """
    Fixture to create a tmp geopackage file that contains relevant BRO soilmap information
    to test.

    """
    polygons = create_polygons()
    maparea_id = np.arange(len(polygons))
    soilunits = [
        "pVc",  # Peat type
        "hVk",  # Peat type
        "kVc",  # Peat type
        "Vc",  # Peat type
        "AAP",  # Peat type
        "vWp",  # Moerig type
        "iWp",  # Moerig type
        "kWz",  # Moerig type
        "AWv",  # Moerig type
        "Rv01C",  # Buried type
        "pRv81",  # Buried type
        "Mv51A",  # Buried type
        "Mv81A",  # Buried type
        "bEZ23",  # Other type
    ]
    geometries = gpd.GeoDataFrame(
        {"maparea_id": maparea_id, "geometry": polygons}, crs=28992
    )
    soilcodes = gpd.GeoDataFrame({"maparea_id": maparea_id, "soilunit_code": soilunits})

    layers = ["soilarea", "soilarea_soilunit"]
    tables = [geometries, soilcodes]

    outfile = tmp_path / "soilmap.gpkg"
    for layer, table in zip(layers, tables):
        table.to_file(outfile, driver="GPKG", layer=layer, index=False)

    return outfile


@pytest.fixture
def simple_soilmap(simple_soilmap_path):
    return read_soilmap_geopackage(simple_soilmap_path)


@pytest.fixture
def somers_parcels():
    """
    Simple GeoDataFrame with parcels and a CO2 emission to mimic SOMERS input data.

    """
    parcels = np.array(create_polygons())
    parcels = parcels[[0, 1, 4, 5, 6, 10, 11, -1]]
    ids = np.arange(len(parcels))
    co2 = [2700, 1500, 6100, 3200, 7000, 5000, 2250, 4800]

    return gpd.GeoDataFrame(
        zip(ids, co2), columns=["parcel_id", "median"], geometry=parcels, crs=28992
    )
