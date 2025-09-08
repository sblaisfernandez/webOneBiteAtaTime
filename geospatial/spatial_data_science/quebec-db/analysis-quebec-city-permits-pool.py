# %%
from unittest import case
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
import shapely.wkb
import shapely.wkt

# %%
if os.path.exists("./data/quebecCityPermits.csv"):
    quebecCityPermits = gpd.read_file("./data/quebecCityPermits.csv")

# %%
quebecCityPermitsPiscine = quebecCityPermits[
    quebecCityPermits["reason"].str.contains("piscine", case=False)
]

# %%
# Export to  csv format
quebecCityPermitsPiscine.to_csv(
    "./data/quebecCityPermitsPiscine.csv", index=False, encoding="utf-8"
)


# %%

# %%
# Create a new dataframe in the column "reason" contain the substring "Démolition"
quebecCityPermitsPiscineDemolition = quebecCityPermitsPiscine[
    quebecCityPermitsPiscine["reason"].str.contains("Démolition", case=False)
]

# %%
# Remove the row from quebecCityPermitsPiscine where the column "reason" contains "Démolition"
quebecCityPermitsPiscine = quebecCityPermitsPiscine[
    ~quebecCityPermitsPiscine["reason"].str.contains("Démolition", case=False)
]


# %%
def is_same_property(gdf: gpd.GeoDataFrame, series: pd.Series) -> bool:
    """
    Check if two dataframe have the same property.
    """
    # Do the gdf column "work_address" include the series "work_address"?
    if (
        gdf["work_address"].str.contains(series["work_address"])
        and gdf["affected_lots"].str.contains(series["affected_lots"])
        and gdf["borough"].str.contains(series["borough"])
    ):
        return True
    else:
        return False


# %%
quebecCityPermitsPiscine.describe()
# quebecCityPermitsPiscineDemolition.describe()

# %%
# Add a column "isDemolished" to quebecCityPermitsPiscine set to False by default
quebecCityPermitsPiscine["isDemolished"] = False

# %%
# Map over each row in quebecCityPermitsPiscineDemolition and set the column "isDemolished" to True if pool have been installed
for index, row in quebecCityPermitsPiscineDemolition.iterrows():
    isDemolished = is_same_property(quebecCityPermitsPiscine, row)
    quebecCityPermitsPiscine["isDemolished"] = isDemolished

# %%
quebecCityPermitsPiscine.head(50)

# %%
