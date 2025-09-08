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
    "Url": "https://www.donneesquebec.ca/recherche/dataset/25696140-f1da-4729-831e-9904628c43c6/resource/7b463497-bda8-4942-93a7-051ca4125096/download/vdq-zonesagricolespermanentes.csv",
    "format": "csv",
    "filename": "vdq-zonesagricolespermanentes.csv",
    "updated_at": "2025-08-03 03:08:00+00:00",
    "id": "7b463497-bda8-4942-93a7-051ca4125096",
}

target = {
    "format": "csv",
    "filename": "vdq-zonesagricolespermanentes.csv",
    "id": "7b463497-bda8-4942-93a7-051ca4125096",
    "columns": {
        "ID": "id",
        "updated_at": "updated_at",
        "SUPERFICIE": "area",
        "PERIMETRE": "perimeter",
        "GEOMETRIE": "geometry",
    },
}

response = requests.get(source["Url"])
response.raise_for_status()
rawDataframe = pd.read_csv(io.BytesIO(response.content), encoding="utf-8-sig")
newDataframe = rawDataframe.copy()
# %%
newDataframe = newDataframe.rename(
    columns={
        "ID": "id",
        "updated_at": "updated_at",
        "SUPERFICIE": "area",
        "PERIMETRE": "perimeter",
        "GEOMETRIE": "geometry",
    }
)
newDataframe["updated_at"] = source["updated_at"]
newDataframe = newDataframe[["id","updated_at", "area", "perimeter", "geometry"]]

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

newDataframe.to_csv("./data/vdq-zonesagricolespermanentes.csv", index=False)