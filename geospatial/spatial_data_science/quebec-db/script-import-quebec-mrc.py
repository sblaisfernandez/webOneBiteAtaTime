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
    updated_at="2021-04-15 08:03:00",
    format=".zip",
    layers= ['arron_s', 'comet_s', 'arron_l', 'comet_l', 'mrc_l', 'munic_l', 'regio_l', 'mrc_s', 'munic_s', 'regio_s'],
    epsg= "EPSG:4326",
    columns_of_interest = ["RES_CO_REG", "RES_NM_REG", "geometry"]
)
target = SimpleNamespace(
    wantedRegion="Capitale-Nationale",
    columns=[],
    precision=0.0000001,
    filename="./data/administrative_regions_capitale_nationale.csv",
        wantedColumns=[
        "MRS_CO_MRC",
        "MRS_NM_MRC",
        "MRS_CO_REG",
        "geometry",
    ],
    finalColumns=[
        "mrc_code",
        "mrc_name",
        "administrative_regions",
        "updated_at",
        "geom",
    ],
)

if os.path.exists(destination.path):
    municipalities_raw = gpd.read_file(destination.path, layer=source.layers[7])
    print("Reading layers from local folder:", destination.path)

else:
    print("Fetching layers from remote URL")
    response = requests.get(source.url)
    response.raise_for_status()
    zip_file = zipfile.ZipFile(io.BytesIO(response.content))
    zip_file.extractall(path=destination.dataFolderRelativePath)
    layers = fiona.listlayers(destination.path)
    municipalities_raw = gpd.read_file(destination.path, layer=source.layers[7])
    municipalities_raw.to_csv("./data/quebec-municipalities.csv", index=False)


mrc_df = municipalities_raw.copy()
mrc_df = municipalities_raw[target.wantedColumns]
# rename columns
mrc_df = mrc_df.rename(columns={
    "MRS_CO_MRC": "mrc_code",
    "MRS_NM_MRC": "mrc_name",
    "MRS_CO_REG": "administrative_regions",
    "geometry": "geom",
})
mrc_df["updated_at"] = source.updated_at
mrc_df = mrc_df[target.finalColumns]
# %%
# convert mrc_df to GeoDataframe
mrc_gdf = gpd.GeoDataFrame(mrc_df, geometry="geom", crs=source.epsg)
# %%

# %%
# export mrc_gdf to file
mrc_gdf.to_csv("./data/quebec-mrc.csv", index=False)

# %%
mrc_gdf.plot()

# %%
