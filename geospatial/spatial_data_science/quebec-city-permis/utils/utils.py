from io import StringIO
import geopandas as gpd
import pandas as pd
import requests


def get_data_from_url(url: str) -> pd.DataFrame:
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        if response.encoding != "utf-8":
            response.encoding = "utf-8"

        text = response.text

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None
    except UnicodeDecodeError as e:
        print(f"Decoding error: {e}. Try a different encoding.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

    csv_data = StringIO(text)
    df = pd.read_csv(csv_data, sep=",")
    return df


def replace_longitude_latitude_with_geometry(df: pd.DataFrame) -> gpd.GeoDataFrame:
    """
    Replace the longitude and latitude columns with a geometry column.
    """

    # truncate the longitude and latitude columns to 7 decimal places
    df["LONGITUDE"] = df["LONGITUDE"].round(7)
    df["LATITUDE"] = df["LATITUDE"].round(7)

    # Create a GeoPanda dataframe from the df
    gdf = gpd.GeoDataFrame(df, geometry=None)
    gdf["GEOMETRY"] = gpd.points_from_xy(
        df["LONGITUDE"], df["LATITUDE"], crs="EPSG:4326"
    )
    gdf = gdf.drop(columns=["LONGITUDE", "LATITUDE"])

    # Validate of the column geometry is valid
    if not gdf["GEOMETRY"].is_valid.all():
        print("Invalid geometry found in the dataframe.")
    else:
        print("All geometries are valid.")
        type(gdf)
        return gdf


def convert_str_to_datetime(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """
    Convert a column of date in string to datetime format and return the series.
    """
    try:
        df[column_name] = pd.to_datetime(df[column_name], errors="coerce")
        print("Successfully converted column to datetime format.")
        return df
    except Exception as e:
        print(f"Error converting {column_name} to datetime: {e}")
        return pd.DataFrame()
