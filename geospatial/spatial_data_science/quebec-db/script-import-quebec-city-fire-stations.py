# %%
import os
from types import SimpleNamespace
from wsgiref import headers
from pydantic_core import Url
from dotenv import find_dotenv, load_dotenv
from folium import Map
from io import StringIO
from shapely.geometry import Point
from supabase import create_client, Client
import geopandas as gpd
import pandas as pd
import requests
from shapely import wkt

# %%
# Constants
source = SimpleNamespace(
    crs="EPSG:4326",
    filename="./data/MSP_CASERNE_PUBLIC.csv",
    format="csv",
    id="c3d81446-d2c0-43c2-b3ab-8e05a1af4589",
    updated_at="2025-08-27 06:58:00",
    Url="https://geoegl.msp.gouv.qc.ca/apis/wss/incendie.fcgi?service=wfs&version=1.1.0&request=getfeature&typename=MSP_CASERNE_PUBLIC&outputformat=CSV",
)
capitalNational = SimpleNamespace(
    sourcePath="./data/administrative_regions_capitale_nationale.csv",
    crs="EPSG:4326",
    targetPath="./data/fireStationsInCapital.csv"
)
target = SimpleNamespace(
    format="csv",
    filename="MSP_CASERNE_PUBLIC.csv",
    id="c3d81446-d2c0-43c2-b3ab-8e05a1af4589",
    columns={
        "id": "uuid",
        "updated_at": "updated_at",
        "SURFACE": "area",
        "PERIMETRE": "perimeter",
        "GEOMETRIE": "geom",
    },
    precision=0.0000001,
)

# %%
capitalDataFrame = gpd.read_file(capitalNational.sourcePath)
if capitalDataFrame["geom"].dtype == object and isinstance(capitalDataFrame["geom"].iloc[0], str):
    capitalDataFrame["geom"] = capitalDataFrame["geom"].apply(wkt.loads)

crs = getattr(capitalNational, "crs", None) or "EPSG:4326"
capitalGeoDataFrame = gpd.GeoDataFrame(capitalDataFrame, geometry=capitalDataFrame.geom, crs=crs)

# %%
if os.path.exists(source.sourcePath):
    rawDataframe = pd.read_csv(f"{source.sourcePath}", dtype=str)
else:
    response = requests.get(source.Url)
    response.raise_for_status()
    rawDataframe = pd.read_csv(StringIO(response.text), encoding="utf-8")

# %%
newDataframe = rawDataframe.copy()
newDataframe[source.updated_at] = source.updated_at

# %%
if newDataframe['geom'].dtype == object and isinstance(newDataframe['geom'].iloc[0], str):
    newDataframe['geom'] = newDataframe['geom'].apply(wkt.loads)
# If source not defined or lacks crs, set manually
crs = getattr(source, "crs", None) or "EPSG:4326"
newGeoDataFrame = gpd.GeoDataFrame(newDataframe, geometry="geom", crs=crs)

# %%
# Create a dataframe from the fire stations inside the capitalGeoDataFrame polygon
fireStationsInCapital = gpd.sjoin(newGeoDataFrame, capitalGeoDataFrame, how="inner", predicate="within")
# select column 'id_caserne', 'no_caserne', 'adresse', 'nom_ssi', 'updated_at_left', 'geom'
fireStationsInCapital = fireStationsInCapital[['id_caserne', 'no_caserne', 'adresse', 'nom_ssi', 'updated_at_left', 'geom']]
# Rename columns
fireStationsInCapital.columns = ['fire_station_id', 'fire_station_no', 'address', 'fire_service_names', 'updated_at', 'geom']

# %%
# plot fireStationCapital on a map
fireStationsInCapital.plot()

# %%
# Save fireStationInCapital to .csv file
fireStationsInCapital.to_csv(capitalNational.targetPath, index=False)

# %%
# export data to .csv  format
# rawDataframe.to_csv("./data/MSP_CASERNE_PUBLIC.csv", index=False)
# %%
