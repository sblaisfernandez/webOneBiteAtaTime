# %%
import io
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
import shapely

# Constants
source = {
    "Url": "https://www.donneesquebec.ca/recherche/dataset/5b1ae6f2-6719-46df-bd2f-e57a7034c917/resource/11b26afb-8215-4723-8dc5-78c93eec8763/download/vdq-quartier.csv",
    "format": "csv",
    "filename": "vdq-quartier.csv",
    "updated_at": "2025-08-31 05:03:00+00:00",
    "id": "11b26afb-8215-4723-8dc5-78c93eec8763",
}

target = {
    "format": "csv",
    "filename": "vdq-quartier.csv",
    "id": "11b26afb-8215-4723-8dc5-78c93eec8763",
    "columns": {
        "id": "uuid",
        "updated_at": "updated_at",
        "SURFACE": "area",
        "PERIMETRE": "perimeter",
        "GEOMETRIE": "geometry",
    },
}

response = requests.get(source["Url"])
response.raise_for_status()
rawDataframe = pd.read_csv(io.BytesIO(response.content), encoding="utf-8-sig")
newDataframe = rawDataframe.copy()

newDataframe = newDataframe.rename(
    columns={
        "ID": "id",
        "NOM": "name",
        "SUPERFICIE": "area",
        "PERIMETRE": "perimeter",
        "GEOMETRIE": "geometry",
    }
)
newDataframe["updated_at"] = "2025-08-31 05:03:00+00:00"
newDataframe = newDataframe[["id","updated_at", "area", "perimeter", "geometry"]]


# %%
# Validation
validationDf = pd.DataFrame()
validationDf["updated_at_valid"] = pd.to_datetime(newDataframe["updated_at"], errors="coerce").notna().all()
validationDf["is_geometry_valid"] = newDataframe["geometry"].apply(
    lambda geom: (
        geom.is_valid if isinstance(geom, shapely.geometry.base.BaseGeometry) else False
    )
)

if not validationDf["updated_at_valid"].iloc[0]:
    print("Error: Invalid datetime values found.")

if not validationDf["is_geometry_valid"].all():
    print("Error: Invalid geometry found.")

# %%
newDataframe.to_csv("./data/vdq-boroughs.csv", index=False)
