# %%
from utils.utils import (
    convert_str_to_datetime,
    get_data_from_url,
    replace_longitude_latitude_with_geometry,
)
from quebecCityPermitsConfiguration import (
    quebecCityPermitsColumns,
)
from dotenv import find_dotenv, load_dotenv
import geopandas as gpd
import os
import pandas as pd

load_dotenv(dotenv_path="/Users/blais/nplus1/webOneBiteAtaTime/.env")

quebec_city_permits_url = "https://www.donneesquebec.ca/recherche/dataset/879abf6e-c6b2-430a-b44a-16335467c6f6/resource/9555031e-cfc5-4b78-bec9-4ab84b549f67/download/vdq-permis.csv"

# %%
if os.path.exists("./data/quebecCityPermits.csv"):
    quebecCityPermits = gpd.read_file("./data/quebecCityPermits.csv")
else:
    quebecCityPermitsDF: pd.DataFrame = get_data_from_url(quebec_city_permits_url)
    quebecCityPermits = replace_longitude_latitude_with_geometry(quebecCityPermitsDF)
    quebecCityPermits = quebecCityPermits.rename(columns=quebecCityPermitsColumns)
    quebecCityPermits = convert_str_to_datetime(quebecCityPermits, "issue_date")

# %%
quebecCityPermits.head()

# %%
quebecCityPermits.to_csv("./data/quebecCityPermits.csv", index=False)
