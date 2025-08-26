# %%
import geopandas as gpd
import pandas as pd
from shapely.geometry.base import BaseGeometry


# %%
# import file from quebec-city-address.csv
quebecCityAddress = gpd.read_file("./data/quebec-city-address.csv")
quebecProjects = gpd.read_file("./data/18_quebec_real-estate_appartements.csv")

# %%
# split the column quebecProjects['address'] into two columns: 'street' and 'number'
quebecProjects[["civic number", "street"]] = quebecProjects["address"].str.split(
    " ", n=1, expand=True
)
# %%
quebecProjects[["start civic number", "end civic number"]] = quebecProjects[
    "civic number"
].str.split("-", n=1, expand=True)

# %%
quebecProjects.head()
# %%
# Create a column 'start_address'  from the merging of the column of 'start civic number' and 'street'
quebecProjects["start_address"] = (
    quebecProjects["start civic number"].astype(str) + " " + quebecProjects["street"]
)
# %%
# keep only the columns 'start_address', 'number_of_units', 'borough'
quebecProjects = quebecProjects[["start_address", "number_of_units", "borough"]].copy()
# %%
quebecProjects.head()

# %%
# Save quebec project to csv format  to file ./data/18_quebec_real-estate_appartements.csv
quebecProjects.to_csv(
    "./data/18_quebec_real-estate_appartements-clean.csv", index=False, encoding="utf-8"
)

# %%
