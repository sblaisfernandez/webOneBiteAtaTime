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
print("AZURE_MAP_KEY", AZURE_MAP_KEY)


# %%


# %%
def convertGeometryToPoint(row: pd.core.series.Series) -> Point:
    # print("convertGeometryToPoint", row)
    if row.get("geometry"):
        return gpd.GeoSeries(Point())

    query = row["address"]
    url = f"https://atlas.microsoft.com/geocode?api-version=2022-02-01-preview&subscription-key={AZURE_MAP_KEY}&query={query}"
    response = requests.get(url)
    geojson = response.json()
    coordinates = geojson["features"][0]["geometry"]["coordinates"]

    if len(coordinates):
        return Point(coordinates[0], coordinates[1])
    else:
        return Point()


# %%
appartementsLogisQuebec = gpd.read_file(
    "./data/20250524_logisQuebec_appartement-for-rent.geojson"
)
quebecCitBorough = gpd.read_file("./data/vdq-arrondissement.csv")

# %%
appartementsLogisQuebec = appartementsLogisQuebec.drop(columns=["geometry"])
appartementsLogisQuebec["geometry"] = None

appartementsLogisQuebec = gpd.GeoDataFrame(
    {
        "id": appartementsLogisQuebec["id"],
        "created_at": datetime.now(),
        "available_at": appartementsLogisQuebec["_disponibilite"],
        "address": appartementsLogisQuebec["adresse"],
        "borough": appartementsLogisQuebec["ville_ville"],
        "number_of_rooms": appartementsLogisQuebec["piece"],
        "number_of_bedrooms": appartementsLogisQuebec["chambre_coucher"],
        "area": appartementsLogisQuebec["superficie"],
        "description": appartementsLogisQuebec["_short_description"],
        "price_CAD": appartementsLogisQuebec["_prix_demande"],
        "url": appartementsLogisQuebec["_url"],
        "source": "logisQuebec",
        "geometry": appartementsLogisQuebec["geometry"],
    },
    crs="EPSG:4326",
)

# %%
# trim space before and after the value of the column 'address'
appartementsLogisQuebec["address"] = appartementsLogisQuebec["address"].apply(
    lambda x: str(x).strip()
)

# %%
appartementsLogisQuebec["price_CAD"] = appartementsLogisQuebec["price_CAD"].apply(
    lambda x: str(x).replace("$", "").strip()
)
#  Add the string 'Quebec, city, Qc' to each cell of the column 'address'
appartementsLogisQuebec["address"] = appartementsLogisQuebec["address"].apply(
    lambda x: f"{x}, Québec, QC"
)

# %%
# Remove string '(Québec)' from the column "borough"
appartementsLogisQuebec["borough"] = appartementsLogisQuebec["borough"].apply(
    lambda x: x.replace("(Québec)", "").strip()
)
# %%
# Convert DataFrame to GeoDataFrame
quebecCitBorough["GEOMETRIE"] = quebecCitBorough["GEOMETRIE"].apply(wkt.loads)
quebecCitBorough = gpd.GeoDataFrame(
    quebecCitBorough, geometry="GEOMETRIE", crs="EPSG:4326"
)
appartementsLogisQuebec["geometry"] = appartementsLogisQuebec["geometry"].apply(
    wkt.loads
)
appartementsLogisQuebec = gpd.GeoDataFrame(
    appartementsLogisQuebec, geometry="geometry", crs="EPSG:4326"
)
# Remove string (Québec) from the column "borough"
appartementsLogisQuebec["borough"] = appartementsLogisQuebec["borough"].apply(
    lambda x: x.replace("(Québec)", "").strip()
)

# %%
# export the GeoDataFrame to a CSV file
# appartementsLogisQuebec.to_csv(
#     "./data/20250524-logisquebec-appartements-for-rent-clean.csv",
#     index=False,
#     encoding="utf-8",
# )

# %%
# Apply the convertGeometryToPoint function to each row of the GeoDataFrame
appartementsLogisQuebec["geometry"] = appartementsLogisQuebec.apply(
    convertGeometryToPoint, axis=1
)

# %%
# export appartementsLogisQuebec to a CSV file
appartementsLogisQuebec.to_csv(
    "./data/20250524-logisquebec-appartements-for-rent-clean-geocoded.csv",
    index=False,
    encoding="utf-8",
)

# %%

# %%
# appartementsLogisQuebec.head()
appartementsLogisQuebec.explore()
