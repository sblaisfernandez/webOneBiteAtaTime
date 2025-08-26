# %%
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point  # type: ignore
from shapely import wkt
from shapely.geometry.base import BaseGeometry
import requests
from io import StringIO
import uuid
from supabase import create_client, Client
from dotenv import find_dotenv, load_dotenv
import os
from datetime import datetime

# from utils import convertGeometryToPoint  # type: ignore
load_dotenv(dotenv_path="/Users/blais/nplus1/webOneBiteAtaTime/.env")
AZURE_MAP_KEY = os.getenv("AZURE_MAP_KEY")
# %%
# read json file
kangalouJson = pd.read_json("./data/20250524_kangalou_featuredListings.json")
kangalouJson.head(20)


# %%
# Map ove each row of KangalouJson the add a row to Geopandas DataFrame with the following columns:
# - kangalou_id: from id: a random uuid
# - created_at: from the 2025-05-24T00:00:00Z
# - available_at: None
# - address: from the "address" column
# latitude: from the "lt" properties
# longitude: from the "lg" properties
# number_of_rooms: from the "ai" properties
# price_CAD: from 'mc' properties
# url: from the "url" properties
value = kangalouJson["featuredListings"].apply(
    lambda row: {
        "kangalou_id": row["id"],
        "created_at": datetime.fromisoformat("2025-05-24T00:00:00"),
        "available_at": None,
        # "address": row["address"],
        "latitude": row["lt"],
        "longitude": row["lg"],
        "number_of_rooms": row["ai"],
        "price_CAD": row["mc"],
        "url": row["l"],
    }
)

# %%
kangalouListings = pd.DataFrame(value.tolist())
kangalouListings.head(20)

# %%
# convert kangalouListings to a GeoDataFrame
kangalouListings = gpd.GeoDataFrame(
    kangalouListings,
    geometry=gpd.points_from_xy(
        kangalouListings["longitude"], kangalouListings["latitude"]
    ),
    crs="EPSG:4326",
)
# %%
kangalouListings.explore()
# %%
