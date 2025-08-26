# %%
from dotenv import find_dotenv, load_dotenv
from folium import Map
from io import StringIO
from shapely.geometry import Point

# from supabase import create_client, Client
import fiona
import folium
import geopandas as gpd
import os
import pandas as pd
import requests, zipfile, io
import shapely
import uuid

dataFolderRelativePath = "./data"
load_dotenv(dotenv_path="/Users/blais/nplus1/webOneBiteAtaTime/.env")

#  %%
# quebecProjects = gpd.read_file(
#     "./data/18_quebec_real-estate_appartements-clean-geocoded.csv"
# )
projects = gpd.read_file("./data/20250520-quebec-real-estate-projects-merged.csv")

# %%

# %%
adminBoundariesUrl = "https://diffusion.mern.gouv.qc.ca/Diffusion/RGQ/Vectoriel/Theme/Local/SDA_20k/FGDB/SDA.gdb.zip"
response = requests.get(adminBoundariesUrl)
response.raise_for_status()
zip_file = zipfile.ZipFile(io.BytesIO(response.content))
zip_file.extractall(path=dataFolderRelativePath)
adminBoundariesPath = dataFolderRelativePath + "/SDA.gdb"
# layers = fiona.listlayers(adminBoundariesPath)

# %%
communautéMétropolitain = gpd.read_file(adminBoundariesPath, layer="comet_s")

# %%

# %%
communautéMétropolitain.explore()
# Get 'Communauté métropolitaine de Québec' from the column 'CMS_NM_COM' CMD
CMQ = communautéMétropolitain[
    communautéMétropolitain["CMS_NM_COM"] == "Communauté métropolitaine de Québec"
]
CMQ.head()

# %%
# Select the column 'CMS_NO_IND', 'CMS_DE_IND', 'CMS_CO_COM', CMS_NM_COM and 'geometry' from CMQ
CMQ = CMQ[["CMS_NO_IND", "CMS_DE_IND", "CMS_CO_COM", "CMS_NM_COM", "geometry"]]
# Export CMQ to a csv file
CMQ.to_csv(
    "./data/20250520-quebec-communauté-métropolitaine.csv",
    index=False,
    encoding="utf-8",
)
#  %%
# Map over each row in quebecProjects then add each row to projects
# for index, row in quebecProjects.iterrows():
#     new_row = {
#         "id": str(uuid.uuid4()),
#         "name": None,
#         "address": row["address"],
#         "number_of_units": row["number_of_units"],
#         "borough": row["borough"],
#         "date_accepted_by_city": None,
#         "geometry": row["geometry"],
#     }

#     dataFrame = pd.DataFrame([new_row])
#     projects = pd.concat([projects, dataFrame], ignore_index=True)
# %%
projects["geometry"] = projects["geometry"].apply(shapely.wkt.loads)
projects = gpd.GeoDataFrame(projects, geometry="geometry", crs="EPSG:4326")

print(type(projects["geometry"]))
# %%

# %%
# projects.to_csv(
#     "./data/20250520-quebec-real-estate-projects-merged.csv",
#     index=False,
#     encoding="utf-8",
# )

# %%
# some all value of the column 'number_of_units' in projects
# projects["number_of_units"] = pd.to_numeric(
#     projects["number_of_units"], errors="coerce"
# )
# print(projects["number_of_units"].sum())
# %%
