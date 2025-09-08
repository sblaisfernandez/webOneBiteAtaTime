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
import shapely.wkb
import shapely.wkt

# %%
if os.path.exists("./data/quebecCityPermits.csv"):
    quebecCityPermits = gpd.read_file("./data/quebecCityPermits.csv")
# %%
quebecCityPermits.head()


# %%
quebecCityPermits2024 = quebecCityPermits[
    quebecCityPermits["issue_date"].dt.year == 2024
]
quebecCityPermits2024.describe()

# %%
# How many rows are in the year 2025
quebecCityPermits2025 = quebecCityPermits[
    quebecCityPermits["issue_date"].dt.year == 2025
]
quebecCityPermits2025.describe()


# %%
quebecCityPermits2024And2025 = pd.concat(
    [quebecCityPermits2024, quebecCityPermits2025],
    ignore_index=True,
)
quebecCityPermits2024And2025.describe()


# %%
quebecCityPermitsByBorough = (
    quebecCityPermits.groupby("borough").size().reset_index(name="count")
)
quebecCityPermitsByBorough.head()

# %%

# %%
## Group quebecCityPermits by the column "domain" and count the number of permits in each domain
quebecCityPermitsByDomain = (
    quebecCityPermits.groupby("domain").size().reset_index(name="count")
)
quebecCityPermitsByDomainHead = quebecCityPermitsByDomain.head(50)
quebecCityPermitsByDomainHead


# %%
# Groupe quebecCityPermits by the column "reason" and count the number of permits in each reason
quebecCityPermitsByReason = (
    quebecCityPermits.groupby("reason").size().reset_index(name="count")
)
quebecCityPermitsByReasonHead = quebecCityPermitsByReason.head(50)
quebecCityPermitsByReasonHead

# %%
# How many pool have been add to the quebec city? territory during the last 5 years?
quebecCityPermits["issue_date"] = pd.to_datetime(quebecCityPermits["issue_date"])
last_5_years = pd.Timestamp.now() - pd.DateOffset(years=5)
recent_pools = quebecCityPermits[
    (quebecCityPermits["issue_date"] >= last_5_years)
    & (quebecCityPermits["type_of_work"] == "Installation de piscine")
]
recent_pools_count = recent_pools.shape[0]
