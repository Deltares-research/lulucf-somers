import geopandas as gpd
import pytest
from numpy.testing import assert_array_almost_equal, assert_array_equal

from lusos.readers import BroSoilmap, read_soilmap_geopackage


class TestBroSoilmap:
    @pytest.mark.unittest
    def test_read_geometries(self, simple_soilmap_path):
        with BroSoilmap(simple_soilmap_path) as sm:
            soilmap = sm.read_geometries()
            assert isinstance(soilmap, gpd.GeoDataFrame)


@pytest.mark.unittest
def test_read_soilmap_geopackage(simple_soilmap_path):
    soilmap = read_soilmap_geopackage(simple_soilmap_path)
    assert isinstance(soilmap, gpd.GeoDataFrame)

    expected_columns = ["maparea_id", "soilunit_code"]
    assert all([col in soilmap.columns for col in expected_columns])

    # Test with bounding box selection
    soilmap = read_soilmap_geopackage(simple_soilmap_path, bbox=(0, 0, 2, 2))
    assert isinstance(soilmap, gpd.GeoDataFrame)
    assert_array_almost_equal(soilmap.total_bounds, [0, 0, 2.81176471, 3.00208333])
    assert_array_equal(soilmap["maparea_id"], [4, 6, 7, 8, 9, 13])
