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
from shapely.geometry import Point
from supabase import create_client, Client
import geopandas as gpd
import pandas as pd
import requests
from types import SimpleNamespace

# Constants
# dataFolderRelativePath =
destination = SimpleNamespace(
    dataFolderRelativePath="./data",
    path= './data/SDA.gdb'
)
source = SimpleNamespace(
    url="https://diffusion.mern.gouv.qc.ca/Diffusion/RGQ/Vectoriel/Theme/Local/SDA_20k/FGDB/SDA.gdb.zip",
    updatedAt="2021-04-15T08:03:00+00:00",
    format=".zip",
    layer= "regio_s",
    epsg= "EPSG:4326",
    columns_of_interest = ["RES_CO_REG", "RES_NM_REG", "geometry"]
)
target = SimpleNamespace(
    wantedRegion="Capitale-Nationale",
    columns=[]
)
target_columns_name = {
    "RES_CO_REG": "region_id",
    "RES_NM_REG": "name",
    "geometry": "geom",
}
# %%
if os.path.exists(destination.path):
    print("Reading layers from local folder:", destination.path)
else:
    print("Fetching layers from remote URL")
    response = requests.get(source.url)
    response.raise_for_status()
    zip_file = zipfile.ZipFile(io.BytesIO(response.content))
    zip_file.extractall(path=destination.dataFolderRelativePath)

layers = fiona.listlayers(destination.path)
administrativeRegions = gpd.read_file(destination.path, layer=source.layer)
administrativeRegions = administrativeRegions.to_crs(source.epsg)

capitalNationale = administrativeRegions[
    administrativeRegions["RES_NM_REG"] == target.wantedRegion
]
administrativeRegions = administrativeRegions[source.columns_of_interest]
administrativeRegions = administrativeRegions.rename(columns=target_columns_name)
administrativeRegions["updated_at"] = source.updatedAt

# %%
# Add a column 'is_valid_geom' if the column 'geom' is valid
validation = pd.DataFrame()
validation["is_valid_geom"] = administrativeRegions["geom"].apply(
    lambda geom: geom.is_valid
)

# %%
administrativeRegions.to_csv("./data/administrative_regions.csv", index=False)

# %%
