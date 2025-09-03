# %%
import os
from wsgiref import headers
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
        location = geocode_response[0]['geometry']['location']
        point = Point(location['lng'], location['lat'])
        point = set_precision(point, precision)
        return point
    else:
        return None


# Constants
load_dotenv(dotenv_path="/Users/blais/nplus1/webOneBiteAtaTime/.env")
GOOGLE_MAP_KEY = os.getenv("GOOGLE_MAP_KEY")

destination = SimpleNamespace(dataFolderRelativePath="./data", path="./data/SDA.gdb")
source = SimpleNamespace(
    url="https://donneesouvertes.affmunqc.net/repertoire/MUN.csv",
    updatedAt="2025-09-03 07:00:00",
    format=".csv",
    epsg="EPSG:4326",
    metadata_url= "https://www.donneesquebec.ca/recherche/dataset/repertoire-des-municipalites-du-quebec/resource/19385b4e-5503-4330-9e59-f998f5918363",
    columns_of_interest=["RES_CO_REG", "RES_NM_REG", "geometry"],
)
target = SimpleNamespace(
    columns=[], precision=0.0000001, filename="./data/quebec-municipalities-raw.csv"
)

if os.path.exists(target.filename):
    rawDataframe = pd.read_csv(target.filename, dtype=str)
else:
    response = requests.get(source.url)
    response.raise_for_status()
    rawDataframe = pd.read_csv(StringIO(response.text), encoding="utf-8")
    rawDataframe.to_csv(target.filename, index=False)

wantedColumns = ['mcode', 'munnom', 'madr1', 'madr2', 'mcodpos', 'mcourriel', 'mweb', 'mtel','mpopul']
newDataframe = rawDataframe[wantedColumns]
newDataframe = newDataframe.rename(columns={
    "mcode": "municipality_code",
    "munnom": "municipality_name",
    "madr1": "street",
    "madr2": "city",
    "mcodpos": "postal_code",
    "mcourriel": "email",
    "mweb": "website",
    "mtel": "phone",
    "mpopul": "population"
})
# Selection only the row that have a define value at the column 'street'
newDataframe = newDataframe[newDataframe['street'].notna()]
newDataframe['province_code'] = 'QC'
newDataframe['country'] = 'Canada'
newDataframe['address'] = newDataframe['street'] + ', ' + newDataframe['city'] + ', ' + newDataframe['province_code'] + ', ' + newDataframe['country']
# Reorder columns
newDataframe = newDataframe[[
    "municipality_code",
    "municipality_name",
    "address",
    "city",
    "postal_code",
    "phone",
    "email",
    "website",
    "population"
]]

# %%
# gmaps = googlemaps.Client(key=GOOGLE_MAP_KEY)
# geocode_response = gmaps.geocode('56, rue Martel, Chambly, QC, Canada')
# location = geocode_response[0]['geometry']['location'] if geocode_response else None
# # Generate a valid Geopandas geometry value from location
# point = Point(location['lng'], location['lat'])
# point = set_precision(point, target.precision)


# %%
# map over each address in the newDataframe
newDataframe['geom'] = newDataframe['address'].apply(lambda row: geocode_address(row, gmaps))

# %%
# Convert newDataframe to a GeoDataframe
newGeoDataframe = gpd.GeoDataFrame(newDataframe, geometry='geom', crs="EPSG:4326")
# export newDataframe to a .csv
newGeoDataframe.to_csv("./data/quebec-municipalities-geocoded.csv")

# %%
newGeoDataframe.plot()