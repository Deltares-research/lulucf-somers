import sqlite3

import pandas as pd
import pytest
from numpy.testing import assert_array_equal

from lusos.readers import Geopackage


class TestGeopackage:
    @pytest.mark.unittest
    def test_get_connection(self, simple_soilmap_path):
        gp = Geopackage(simple_soilmap_path)
        gp.get_connection()
        assert isinstance(gp.connection, sqlite3.Connection)

    @pytest.mark.unittest
    def test_layers(self, simple_soilmap_path):
        gp = Geopackage(simple_soilmap_path)
        layers = gp.layers()
        expected_layers = ["soilarea", "soilarea_soilunit"]
        assert_array_equal(layers, expected_layers)

    @pytest.mark.unittest
    def test_context_manager(self, simple_soilmap_path):
        gp = Geopackage(simple_soilmap_path)
        assert gp.connection is None
        with gp:
            assert isinstance(gp.connection, sqlite3.Connection)
        assert gp.connection is None

    @pytest.mark.unittest
    def test_get_cursor(self, simple_soilmap_path):
        with Geopackage(simple_soilmap_path) as gp:
            cursor = gp.get_cursor()
            assert isinstance(cursor, sqlite3.Cursor)

    @pytest.mark.unittest
    def test_get_column_names(self, simple_soilmap_path):
        with Geopackage(simple_soilmap_path) as gp:
            columns = gp.get_column_names("soilarea_soilunit")
            assert_array_equal(columns, ["fid", "maparea_id", "soilunit_code"])

    @pytest.mark.unittest
    def test_read_table(self, simple_soilmap_path):
        test_table = "soilarea_soilunit"
        with Geopackage(simple_soilmap_path) as gp:
            table = gp.read_table(test_table)
            assert isinstance(table, pd.DataFrame)
            assert_array_equal(table.columns, ["fid", "maparea_id", "soilunit_code"])

            table = gp.table_head(test_table)
            assert len(table) == 5
