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

# Constants
adminBoundariesUrl = 'https://diffusion.mern.gouv.qc.ca/Diffusion/RGQ/Vectoriel/Theme/Local/SDA_20k/FGDB/SDA.gdb.zip'
dataFolderRelativePath = './data'

if os.path.exists(dataFolderRelativePath + '/SDA.gdb'):
    # layers = fiona.listlayers(dataFolderRelativePath + '/SDA.gdb')
    print("Reading layers from local folder:", dataFolderRelativePath + '/SDA.gdb')
else:
    print("Fetching layers from remote URL")
    response = requests.get(adminBoundariesUrl)
    response.raise_for_status()
    zip_file = zipfile.ZipFile(io.BytesIO(response.content))
    zip_file.extractall(path=dataFolderRelativePath)

path = dataFolderRelativePath + '/SDA.gdb'
layers = fiona.listlayers(path)
administrativeRegions = gpd.read_file(path, layer='regio_s')

capitalNationale = administrativeRegions[administrativeRegions['RES_NM_REG'] == 'Capitale-Nationale']
capitalNationale = capitalNationale.to_crs('EPSG:4326')

# %%
columns_of_interest = ['RES_CO_REG', 'RES_NM_REG', 'geometry']
administrativeRegions = administrativeRegions[columns_of_interest]
# Rename columns to match the database schema
administrativeRegions = administrativeRegions.rename(columns={
    'RES_CO_REG': 'id',
    'RES_NM_REG': 'name',
    'geometry': 'geom'
})
# Add a column 'is_valid_geom' if the column 'geometry' is valid
validation = pd.DataFrame()
validation['is_valid_geom'] = administrativeRegions['geometry'].apply(lambda geom: geom.is_valid)

# %%
administrativeRegions.to_csv("./data/administrative_regions.csv", index=False)
# %%
