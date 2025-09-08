# %%
from datetime import datetime
import os
from wsgiref import headers
import numpy as np
from pydantic_core import Url
from dotenv import find_dotenv, load_dotenv
from folium import Map
from io import StringIO
from shapely import set_precision
from shapely.geometry import Point
from supabase import create_client, Client
import geopandas as gpd
import pandas as pd
import requests
from types import SimpleNamespace
import googlemaps


# Functions
def geocode_address(address, gmaps_client, precision=0.0000001):
    geocode_response = gmaps_client.geocode(address)
    if geocode_response:
        location = geocode_response[0]["geometry"]["location"]
        point = Point(location["lng"], location["lat"])
        point = set_precision(point, precision)
        return point
    else:
        return None


def run_gmaps_geocoding(df: pd.DataFrame):
    try:
        gmaps = googlemaps.Client(key=GOOGLE_MAP_KEY)
        print("Google Maps client initialized.")
    except Exception as e:
        print("Error initializing Google Maps client:", e)
        return df

    print("Geocoding started at:", datetime.now())
    df["geom"] = df["address"].apply(lambda row: geocode_address(row, gmaps))
    print("Geocoding ended at:", datetime.now())
    return df


def rename_columns(df: pd.DataFrame):
    columns_mapping = {
        "mcode": "municipality_code",
        "munnom": "municipality_name",
        "madr1": "street",
        "madr2": "city",
        "mcodpos": "postal_code",
        "mcourriel": "email",
        "mweb": "website",
        "mtel": "phone",
        "mpopul": "population",
    }
    return df.rename(columns=columns_mapping)


def generate_address(df: pd.DataFrame):
    df["province_code"] = "QC"
    df["country"] = "Canada"
    df["address"] = (
        df["street"]
        + ", "
        + df["city"]
        + ", "
        + df["province_code"]
        + ", "
        + df["country"]
    )
    return df


def reorder_columns(df: pd.DataFrame, columns: list = []):
    return df[columns]


def valid_geom(gpd: gpd.GeoDataFrame, columnName="geom"):
    """
    Default value of columnName is 'geom'.
    """
    # PPrint "All geom are valid " if all geom are valid
    if gpd[columnName].is_valid.all():
        print("All geom are valid")
    else:
        print("At least one geom are not valid")

# %%
def convert_column_to_int_nullable(df, col):
    s = pd.to_numeric(df[col], errors="coerce")  # strings -> numeric, bad -> NaN
    s = s.replace([np.inf, -np.inf], pd.NA)  # infinities -> NA
    df[col] = s.astype("Int64")  # pandas nullable int
    return df

# %%
# Constants
load_dotenv(dotenv_path="/Users/blais/nplus1/webOneBiteAtaTime/.env")
GOOGLE_MAP_KEY = os.getenv("GOOGLE_MAP_KEY")

destination = SimpleNamespace(dataFolderRelativePath="./data", path="./data/SDA.gdb")
source = SimpleNamespace(
    url="https://donneesouvertes.affmunqc.net/repertoire/MUN.csv",
    updated_at="2025-09-03 07:00:00",
    format=".csv",
    epsg="EPSG:4326",
    metadata_url="https://www.donneesquebec.ca/recherche/dataset/repertoire-des-municipalites-du-quebec/resource/19385b4e-5503-4330-9e59-f998f5918363",
    columns_of_interest=["RES_CO_REG", "RES_NM_REG", "geometry"],
)
target = SimpleNamespace(
    columns=[],
    precision=0.0000001,
    filename="./data/quebec-municipalities-city-hall-geocoded.csv",
    wantedColumns=[
        "mcode",
        "munnom",
        "madr1",
        "madr2",
        "mcodpos",
        "mcourriel",
        "mweb",
        "mtel",
        "mpopul",
    ],
    finalColumns=[
        "municipality_code",
        "municipality_name",
        "address",
        "city",
        "postal_code",
        "phone",
        "email",
        "website",
        "population",
        "updated_at",
        "city_hall_location",
    ],
)

# %%
if os.path.exists(target.filename):
    rawDataframe = pd.read_csv(target.filename, dtype=str)
else:
    response = requests.get(source.url)
    response.raise_for_status()
    rawDataframe = pd.read_csv(StringIO(response.text), encoding="utf-8")
    rawDataframe.to_csv(target.filename, index=False)

# %%
newDataframe = rawDataframe[target.wantedColumns]
newDataframe = rename_columns(newDataframe)
newDataframe = newDataframe[newDataframe["street"].notna()]
newDataframe = reorder_columns(
    [
        "municipality_code",
        "municipality_name",
        "address",
        "city",
        "postal_code",
        "phone",
        "email",
        "website",
        "population",
    ]
)

# %%
if os.path.exists(target.filename):
    newGeoDataframe = gpd.read_file(target.filename)
else:
    newGeoDataframe = gpd.GeoDataFrame(newDataframe, geometry="city_hall_location", crs="EPSG:4326")
    # newGeoDataframe = run_gmaps_geocoding(newDataframe)
    newGeoDataframe.to_csv(target.filename, index=False)

# %%
newGeoDataframe["updated_at"] = source.updated_at
newGeoDataframe = newGeoDataframe[target.finalColumns]
convert_column_to_int_nullable(newGeoDataframe, "population")
valid_geom(newGeoDataframe)

# %%
newGeoDataframe.to_csv(target.filename, index=False)