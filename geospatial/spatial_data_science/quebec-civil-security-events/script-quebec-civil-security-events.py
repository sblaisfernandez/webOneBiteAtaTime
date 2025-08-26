# %%
from dotenv import find_dotenv, load_dotenv
from folium import Map
from io import StringIO
from shapely.geometry import Point
from supabase import create_client, Client
import folium
import geopandas as gpd
import os
import sys
import pandas as pd
import requests

# Get the absolute path of the current file's directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# Construct the path to the parent directory (project/)
parent_dir = os.path.join(current_dir, "..")
# Add the parent directory to sys.path
sys.path.insert(
    0, parent_dir
)  # Use insert(0, ...) to add it at the beginning for higher priority

# Now you can import the function
from utils.utils import replace_column_by_geometry_column

load_dotenv(dotenv_path="/Users/blais/nplus1/webOneBiteAtaTime/.env")

# %%
dataSource = {
    "url": "https://geoegl.msp.gouv.qc.ca/apis/wss/historiquesc.fcgi?service=wfs&version=1.1.0&request=getfeature&typename=msp_risc_evenements_public&outputformat=CSV",
    "format": "csv",
    "metadata_url": "https://www.donneesquebec.ca/recherche/dataset/evenements-de-securite-civile/resource/8a707be3-2452-43b2-be72-fb5926876c72",
    "updatedAt": "2025-05-09 09:40Z",
    "identifier": "8a707be3-2452-43b2-be72-fb5926876c72",
}

# %%
response = requests.get(dataSource["url"])
response.raise_for_status()
# Read the CSV data into a Pandas DataFrame
csv_data = StringIO(response.text)
rawDataframe = pd.read_csv(csv_data)

# %%
# Sort the dataframe by the date of the column "date_signalement"
rawDataframe = rawDataframe.sort_values(by="date_signalement")
# rawDataframe.head()
# Get the dimension of the dataframe
rawDataframe.shape
# %%
# What is the time frame based on the column "date_signalement"
time_frame = rawDataframe["date_signalement"].agg(["min", "max"])
print(time_frame)

# %%
newDataFrame = replace_column_by_geometry_column(rawDataframe, ["coord_x", "coord_y"])

newDataFrame.head(10)

# %%
# Plot the newDataFrame on a map
newDataFrame.plot()
# %%
