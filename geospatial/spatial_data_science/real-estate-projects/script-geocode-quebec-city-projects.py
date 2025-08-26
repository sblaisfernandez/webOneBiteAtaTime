# %%
from dotenv import find_dotenv, load_dotenv
from folium import Map
from io import StringIO
from shapely.geometry import Point
from supabase import create_client, Client
import folium
import geopandas as gpd
import os
import pandas as pd
import requests
import shapely
import shapely.wkt

load_dotenv(dotenv_path="/Users/blais/nplus1/webOneBiteAtaTime/.env")
AZURE_MAP_KEY = os.getenv("AZURE_MAP_KEY")

#  %%
quebecProjects = gpd.read_file(
    "./data/18_quebec_real-estate_appartements-clean-geocoded.csv"
)
projects = gpd.read_file("./data/20250520-quebec-real-estate-projects-cleanup.csv")


# %%
def convertGeometryToPoint(row: pd.core.series.Series) -> Point:
    if row.get("geometry"):
        return gpd.GeoSeries(Point())

    url = f"https://atlas.microsoft.com/geocode?api-version=2022-02-01-preview&subscription-key={AZURE_MAP_KEY}&query={row["start_address"]}"
    response = requests.get(url)
    geojson = response.json()
    coordinates = geojson["features"][0]["geometry"]["coordinates"]

    if len(coordinates):
        return Point(coordinates[0], coordinates[1])
    else:
        return Point()


# %%
# If your geometry column contains WKT strings:
quebecProjects["geometry"] = quebecProjects["geometry"].apply(shapely.wkt.loads)
quebecProjects = gpd.GeoDataFrame(quebecProjects, geometry="geometry", crs="EPSG:4326")
projects["geometry"] = projects["geometry"].apply(shapely.wkt.loads)
projects = gpd.GeoDataFrame(projects, geometry="geometry", crs="EPSG:4326")

# %%
myCustomMap = Map(location=[46.8139, -71.2082], tiles="OpenStreetMap", zoom_start=12)

# Add a layer using quebecProjects and projects to myCustomMap
# for each row in quebecProjects, add a marker to the map
for _, row in quebecProjects.iterrows():
    if row["geometry"]:
        myCustomMap.add_child(
            folium.Marker(
                location=[row["geometry"].y, row["geometry"].x],
                popup=row["start_address"],
                icon=folium.Icon(color="red"),
            )
        )
# for each row in projects add a marker to the map
for _, row in projects.iterrows():
    if row["geometry"]:
        myCustomMap.add_child(
            folium.Marker(
                location=[row["geometry"].y, row["geometry"].x],
                popup=row["number_of_units"],
                icon=folium.Icon(color="blue"),
            )
        )

myCustomMap
