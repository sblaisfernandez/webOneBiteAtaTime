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

# Constants
source = {
    "Url": "https://geoegl.msp.gouv.qc.ca/apis/wss/incendie.fcgi?service=wfs&version=1.1.0&request=getfeature&typename=MSP_CASERNE_PUBLIC&outputformat=CSV",
    format: "csv",
    "filename": "MSP_CASERNE_PUBLIC.csv",
    "updated_at": "2025-08-27 06:58:00+00:00",
    id: "c3d81446-d2c0-43c2-b3ab-8e05a1af4589",
}

target = {
    "format": "csv",
    "filename": "MSP_CASERNE_PUBLIC.csv",
    "id": "c3d81446-d2c0-43c2-b3ab-8e05a1af4589",
    "columns": {
        "id": "uuid",
        "updated_at": "updated_at",
        "SURFACE": "area",
        "PERIMETRE": "perimeter",
        "GEOMETRIE": "geometry",
    },
}


# %%
response = requests.get(source["Url"])
response.raise_for_status()
rawDataframe = pd.read_csv(StringIO(response.text), encoding="utf-8")
rawDataframe["updated_at"] = "2025-08-27 06:58:00+00:00"
# reduce the decimal precision of 'coord_x' and 'coord_y'
rawDataframe['coord_x'] = rawDataframe['coord_x'].round(6)
rawDataframe['coord_y'] = rawDataframe['coord_y'].round(6)
# Create a column geometry from the columns 'coord_x' and 'coord_y'
rawDataframe["geometry"] = rawDataframe.apply(lambda row: Point(row["coord_x"], row["coord_y"]), axis=1)
rawDataframe = rawDataframe.drop(columns=["coord_x", "coord_y"])

# %%
# export data to .csv  format
rawDataframe.to_csv("./data/MSP_CASERNE_PUBLIC.csv", index=False)
# %%
