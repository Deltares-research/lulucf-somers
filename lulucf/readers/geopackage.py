from pathlib import Path

import fiona
import pandas as pd

from lulucf.utils import create_connection


class Geopackage:
    def __init__(self, file: str | Path):
        self.file = file
        self.connection = None

    def __enter__(self):
        self.get_connection()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.connection:
            self.connection = None

    def layers(self):
        return fiona.listlayers(self.file)

    def get_connection(self):
        self.connection = create_connection(self.file)

    def get_cursor(self):
        return self.connection.cursor()

    def get_column_names(self, table: str) -> list:
        """
        Get the column names of a table in the BRO Bodemkaart geopackage.

        Parameters
        ----------
        table : string
            Name of the table to get the column names for.

        Returns
        -------
        columns : list
            List of the column names for the table.

        """
        cursor = self.get_cursor()
        cursor.execute(f"SELECT * FROM {table}")
        columns = [col[0] for col in cursor.description]
        return columns

    def table_head(self, table: str) -> pd.DataFrame:
        """
        Select the first five records from a table the BRO Bodemkaart geopackage.

        Parameters
        ----------
        table : string
            Name of the table to select the first records from.

        Returns
        -------
        pd.DataFrame
            Pandas DataFrame of the first five records.

        """
        cursor = self.get_cursor()
        cursor.execute(f"SELECT * FROM {table} LIMIT 5")
        data = cursor.fetchall()
        return pd.DataFrame(data, columns=self.get_column_names(table))

    def read_table(self, table: str) -> pd.DataFrame:
        """
        Read all data in a specified table of the GeoPackage.

        Parameters
        ----------
        table : str
            _description_

        Returns
        -------
        pd.DataFrame
            _description_
        """
        columns = self.get_column_names(table)
        table = self.query(f"SELECT * FROM {table}", columns)
        return table

    def query(self, query: str, outcolumns: list = None) -> pd.DataFrame:
        """
        Use a custom query on the geopackage to retrieve desired tables.

        Parameters
        ----------
        query : str
            Full string of the SQL query to retrieve the desired table with.
        outcolumns : list, optional
            Specify column names to be used for the output table. The default is
            None.

        Returns
        -------
        pd.DataFrame
            Result DataFrame of the query.

        """
        cursor = self.get_cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        return pd.DataFrame(data, columns=outcolumns)
