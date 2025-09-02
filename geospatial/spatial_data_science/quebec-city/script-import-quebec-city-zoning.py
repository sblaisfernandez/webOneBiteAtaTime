# %%
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

load_dotenv(dotenv_path="/Users/blais/nplus1/webOneBiteAtaTime/.env")
# Constants
adminBoundariesUrl = 'https://diffusion.mern.gouv.qc.ca/Diffusion/RGQ/Vectoriel/Theme/Local/SDA_20k/FGDB/SDA.gdb.zip'

source = {
    "Url": "https://www.donneesquebec.ca/recherche/dataset/a56dfef1-ad07-4b21-9ef7-24a0c553a085/resource/36afc3b9-a6d5-447f-93fa-443f44e94b7c/download/vdq-zonagemunicipalzones.csv",
    format: "csv",
    "filename": "vdq-zonagemunicipalzones.csv",
    "updated_at": "2025-08-03 03:08:00+00:00",
    id: "36afc3b9-a6d5-447f-93fa-443f44e94b7c",
}

target = {
    "format": "csv",
    "filename": "vdq-zonagemunicipalzones.csv",
    "id": "36afc3b9-a6d5-447f-93fa-443f44e94b7c",
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
csv_data = StringIO(response.text)
rawDataframe = pd.read_csv(csv_data, encoding="utf-8")
rawDataframe = rawDataframe.drop(columns=["ï»¿ID"])
rawDataframe = rawDataframe.rename(
    columns={
        "SURFACE": "area",
        "PERIMETRE": "perimeter",
        "GEOMETRIE": "geometry",
    }
)
rawDataframe["updated_at"] = "2025-08-03 03:08:00+00:00"


# %%
# Validation
validationDf = pd.DataFrame()
validationDf["updated_at_valid"] = pd.to_datetime(rawDataframe["updated_at"], errors="coerce").notna().all()
validationDf["is_geometry_valid"] = rawDataframe["geometry"].apply(
    lambda geom: (
        geom.is_valid if isinstance(geom, shapely.geometry.base.BaseGeometry) else False
    )
)

if not validationDf["updated_at_valid"].iloc[0]:
    print("Error: Invalid datetime values found.")

if not validationDf["is_geometry_valid"].all():
    print("Error: Invalid geometry found.")


# %%
rawDataframe.to_csv("./data/vdq-zonagemunicipalzones.csv", index=False)

# %%
# Convert rawDataframe to rawGeoDataframe
# rawGeoDataframe = gpd.GeoDataFrame(rawDataframe, geometry="geometry", crs="EPSG:4326")

# %%
# Create a column 'is_geometry_valid' if the geometry is valid
# Group all the rows GEOMETRIE of value true in a subDataFrame
valid_geometry_df = rawDataframe[rawDataframe["is_geometry_valid"]]
