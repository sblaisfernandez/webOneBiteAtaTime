# %%
import geopandas as gpd
import pandas as pd
from shapely.geometry.base import BaseGeometry
import requests
from io import StringIO
import uuid
from supabase import create_client, Client
from dotenv import find_dotenv, load_dotenv
import os

# %%
# The data from quebec real estate projects come from les constructions résidentiel à la ville de Québec
# extracted from pdf https://www.ville.quebec.qc.ca/gens_affaires/implantation-projets-immobiliers/projets-residentiels/docs/constructions-residentielles.pdf
quebecProjectsCSV = pd.read_csv("./data/quebec-real-estate-projects.csv", sep=",")

# %%
# Generate a uuid() for each row in  quebecProjectsCSV
quebecProjectsCSV["Id"] = quebecProjectsCSV.apply(lambda x: uuid.uuid4(), axis=1)
wkf = gpd.GeoSeries.from_wkt(quebecProjectsCSV["wkf"], crs="EPSG:4326")


# %%
quebecProjects = gpd.GeoDataFrame(
    {
        "Id": quebecProjectsCSV["Id"],
        "name": quebecProjectsCSV["Nom"],
        "borough": quebecProjectsCSV["Arrondissement"],
        "date_accepted_at_city": quebecProjectsCSV["Date"],
        "number_of_units": quebecProjectsCSV["Nombre de logements"],
        "type": quebecProjectsCSV["Type"],
        "promoter": quebecProjectsCSV["Promoteur"],
        "phone": quebecProjectsCSV["Téléphone"],
        "url": quebecProjectsCSV["url"],
        "geometry": wkf,
    },
    crs="EPSG:4326",
)
quebecProjects.head()

# %%
# Safe quebecProjects to .csv
quebecProjects.to_csv("./data/quebec-real-estate-projects-cleanup.csv", index=False)
quebecProjects.explore(column="name", popup=True, tiles="CartoDB positron")


# %%
load_dotenv(dotenv_path="/Users/blais/nplus1/webOneBiteAtaTime/.env")

# %%
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# %%
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# %%
try:
    response = supabase.table("test-table").select("*").execute()
    print(response)
except Exception as e:
    print(f"Error deleting record: {e}")

# %%
