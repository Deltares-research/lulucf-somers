import geopandas as gpd
import pytest

from lulucf.readers import BroSoilmap, read_soilmap_geopackage


class TestBroSoilmap:
    @pytest.mark.unittest
    def test_read_geometries(self, simple_soilmap):
        with BroSoilmap(simple_soilmap) as sm:
            soilmap = sm.read_geometries()
            assert isinstance(soilmap, gpd.GeoDataFrame)


@pytest.mark.unittest
def read_soilmap_geopackage(simple_soilmap):
    soilmap = read_soilmap_geopackage(simple_soilmap)
    assert isinstance(soilmap, gpd.GeoDataFrame)

    expected_columns = ["maparea_id", "normalsoilprofile_id", "soilunit"]
    assert all([col in soilmap.columns for col in expected_columns])
