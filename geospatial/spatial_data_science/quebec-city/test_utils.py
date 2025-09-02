import unittest
from unittest.mock import patch, Mock
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import requests
from io import StringIO
import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(__file__))

from utils.utils import (
    get_data_from_url,
    replace_longitude_latitude_with_geometry,
    convert_str_to_datetime,
)


class TestGetDataFromUrl(unittest.TestCase):
    """Test cases for get_data_from_url function"""

    @patch("utils.utils.requests.get")
    def test_get_data_from_url_success(self, mock_get):
        """Test successful data retrieval from URL"""
        # Mock response
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.encoding = "utf-8"
        mock_response.text = "col1,col2,col3\n1,2,3\n4,5,6\n"
        mock_get.return_value = mock_response

        # Test
        result = get_data_from_url("http://example.com/data.csv")

        # Assertions
        mock_get.assert_called_once_with("http://example.com/data.csv", timeout=10)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 2)
        self.assertEqual(list(result.columns), ["col1", "col2", "col3"])

    @patch("utils.utils.requests.get")
    def test_get_data_from_url_request_exception(self, mock_get):
        """Test handling of request exceptions"""
        mock_get.side_effect = requests.exceptions.RequestException("Connection error")

        with patch("builtins.print") as mock_print:
            result = get_data_from_url("http://example.com/data.csv")

            self.assertIsNone(result)
            mock_print.assert_called_with("Request error: Connection error")

    @patch("utils.utils.requests.get")
    def test_get_data_from_url_http_error(self, mock_get):
        """Test handling of HTTP errors"""
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            "404 Not Found"
        )
        mock_get.return_value = mock_response

        with patch("builtins.print") as mock_print:
            result = get_data_from_url("http://example.com/data.csv")

            self.assertIsNone(result)
            mock_print.assert_called_with("Request error: 404 Not Found")

    @patch("utils.utils.requests.get")
    def test_get_data_from_url_encoding_change(self, mock_get):
        """Test that encoding is changed to utf-8 when different"""
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.encoding = "iso-8859-1"
        mock_response.text = "col1,col2\na,b\n"
        mock_get.return_value = mock_response

        result = get_data_from_url("http://example.com/data.csv")

        self.assertEqual(mock_response.encoding, "utf-8")
        self.assertIsInstance(result, pd.DataFrame)


class TestReplaceLongitudeLatitudeWithGeometry(unittest.TestCase):
    """Test cases for replace_longitude_latitude_with_geometry function"""

    def setUp(self):
        """Set up test data"""
        self.test_df = pd.DataFrame(
            {
                "LONGITUDE": [-71.207889, -71.208123, -71.209456],
                "LATITUDE": [46.815723, 46.816234, 46.817567],
                "NAME": ["Location 1", "Location 2", "Location 3"],
            }
        )

    def test_replace_longitude_latitude_with_geometry_success(self):
        """Test successful conversion of longitude/latitude to geometry"""
        with patch("builtins.print") as mock_print:
            result = replace_longitude_latitude_with_geometry(self.test_df)

            # Check that it returns a GeoDataFrame
            self.assertIsInstance(result, gpd.GeoDataFrame)

            # Check that LONGITUDE and LATITUDE columns are removed
            self.assertNotIn("LONGITUDE", result.columns)
            self.assertNotIn("LATITUDE", result.columns)

            # Check that GEOMETRY column is added
            self.assertIn("GEOMETRY", result.columns)

            # Check that geometry points are created correctly
            self.assertIsInstance(result["GEOMETRY"].iloc[0], Point)

            # Check that coordinates are rounded to 7 decimal places
            point = result["GEOMETRY"].iloc[0]
            self.assertEqual(round(point.x, 7), -71.207889)
            self.assertEqual(round(point.y, 7), 46.815723)

            # Check that all geometries are valid
            mock_print.assert_called_with("All geometries are valid.")

    def test_replace_longitude_latitude_with_geometry_precision(self):
        """Test that longitude and latitude are rounded to 7 decimal places"""
        test_df = pd.DataFrame(
            {
                "LONGITUDE": [-71.20788912345678],
                "LATITUDE": [46.81572387654321],
                "NAME": ["Location 1"],
            }
        )

        with patch("builtins.print"):
            result = replace_longitude_latitude_with_geometry(test_df)

            point = result["GEOMETRY"].iloc[0]
            self.assertEqual(point.x, -71.2078891)
            self.assertEqual(point.y, 46.8157239)

    def test_replace_longitude_latitude_with_geometry_empty_dataframe(self):
        """Test with empty dataframe"""
        empty_df = pd.DataFrame(columns=["LONGITUDE", "LATITUDE", "NAME"])

        with patch("builtins.print") as mock_print:
            result = replace_longitude_latitude_with_geometry(empty_df)

            self.assertIsInstance(result, gpd.GeoDataFrame)
            self.assertEqual(len(result), 0)
            self.assertIn("GEOMETRY", result.columns)
            self.assertNotIn("LONGITUDE", result.columns)
            self.assertNotIn("LATITUDE", result.columns)


class TestConvertStrToDatetime(unittest.TestCase):
    """Test cases for convert_str_to_datetime function"""

    def setUp(self):
        """Set up test data"""
        self.test_df = pd.DataFrame(
            {
                "date_column": ["2023-01-01", "2023-02-15", "2023-03-30"],
                "other_column": ["A", "B", "C"],
            }
        )

    def test_convert_str_to_datetime_invalid_dates(self):
        """Test handling of invalid date strings"""
        test_df = pd.DataFrame(
            {
                "date_column": ["2023-01-01", "invalid-date", "2023-03-30"],
                "other_column": ["A", "B", "C"],
            }
        )

        result = convert_str_to_datetime(test_df, "date_column")

        # Check that invalid dates are converted to NaT
        self.assertTrue(pd.isna(result["date_column"].iloc[1]))
        self.assertFalse(pd.isna(result["date_column"].iloc[0]))
        self.assertFalse(pd.isna(result["date_column"].iloc[2]))

    def test_convert_str_to_datetime_nonexistent_column(self):
        """Test handling of non-existent column"""
        with patch("builtins.print") as mock_print:
            result = convert_str_to_datetime(self.test_df, "nonexistent_column")

            # Should return empty DataFrame on error
            self.assertIsInstance(result, pd.DataFrame)
            self.assertEqual(len(result), 0)
            mock_print.assert_called()

    def test_convert_str_to_datetime_empty_dataframe(self):
        """Test with empty dataframe"""
        empty_df = pd.DataFrame(columns=["date_column"])

        result = convert_str_to_datetime(empty_df, "date_column")

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 0)
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(result["date_column"]))

    def test_convert_str_to_datetime_mixed_formats(self):
        """Test with mixed date formats"""
        test_df = pd.DataFrame(
            {
                "date_column": ["2023-01-01", "01/15/2023", "2023-03-30", "30-03-2023"],
                "other_column": ["A", "B", "C", "D"],
            }
        )

        result = convert_str_to_datetime(test_df, "date_column")

        # pandas should handle some common formats automatically
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(result["date_column"]))
        # Check that at least some dates are parsed correctly
        self.assertFalse(pd.isna(result["date_column"].iloc[0]))


if __name__ == "__main__":
    unittest.main()
