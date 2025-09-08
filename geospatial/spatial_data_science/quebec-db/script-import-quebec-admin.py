# %%
import io
import os
from wsgiref import headers
import zipfile
import fiona
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

# Constants
destination = SimpleNamespace(
    dataFolderRelativePath="./data",
    path= './data/SDA.gdb'
)
source = SimpleNamespace(
    url="https://diffusion.mern.gouv.qc.ca/Diffusion/RGQ/Vectoriel/Theme/Local/SDA_20k/FGDB/SDA.gdb.zip",
    updatedAt="2021-04-15 08:03:00",
    format=".zip",
    layer= "regio_s",
    epsg= "EPSG:4326",
    columns_of_interest = ["RES_CO_REG", "RES_NM_REG", "geometry"]
)
target = SimpleNamespace(
    wantedRegion="Capitale-Nationale",
    columns=[],
    precision=0.0000001,
    filename="./data/administrative_regions_capitale_nationale.csv"
)
target_columns_name = {
    "RES_CO_REG": "region_id",
    "RES_NM_REG": "name",
    "geometry": "geom",
}

if os.path.exists(destination.path):
    print("Reading layers from local folder:", destination.path)
else:
    print("Fetching layers from remote URL")
    response = requests.get(source.url)
    response.raise_for_status()
    zip_file = zipfile.ZipFile(io.BytesIO(response.content))
    zip_file.extractall(path=destination.dataFolderRelativePath)

layers = fiona.listlayers(destination.path)
rawDataframe = gpd.read_file(destination.path, layer=source.layer)
rawDataframe = rawDataframe.to_crs(source.epsg)
# Export rawDataframe to .csv format
rawDataframe.to_csv("./data/administrative_regions_raw.csv", index=False)

newDataframe = rawDataframe.copy()

newDataframe = newDataframe[source.columns_of_interest]
newDataframe = newDataframe.rename(columns=target_columns_name)
newDataframe["updated_at"] = source.updatedAt

# Reorder columns to "region_id", "name", "updated_at", "geom"
newDataframe = newDataframe[["region_id", "name", "updated_at", "geom"]]

# Reduce the precision to 7 digits for the value in the column 'geom'
newDataframe["geom"] = set_precision(newDataframe["geom"], grid_size=target.precision)

# Add a column 'is_valid_geom' if the column 'geom' is valid
validation = pd.DataFrame()
validation["is_valid_geom"] = newDataframe["geom"].apply(
    lambda geom: geom.is_valid
)

capitalDataframe = newDataframe.loc[newDataframe["name"] == target.wantedRegion]
capitalDataframe.to_csv(target.filename, index=False)

# newDataframe.to_csv("./data/administrative_regions.csv", index=False)