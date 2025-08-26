# %%
from utils.utils import (
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
    quebecCityPermits = pd.read_csv("./data/quebecCityPermits.csv")
else:
    quebecCityPermitsRaw = get_data_from_url(quebec_city_permits_url)
    quebecCityPermits = replace_longitude_latitude_with_geometry(quebecCityPermitsRaw)

# %%
# Sort  quebecCityPermits by the column "DATE_DELIVRANCE" in ascending order
# quebecCityPermits = quebecCityPermits.sort_values(by="DATE_DELIVRANCE", ascending=True)
# quebecCityPermits.head(20)
# quebecCityPermits.tail(20)

# %%
quebecCityPermits = quebecCityPermits.rename(columns=quebecCityPermitsColumns)

quebecCityPermits.head()

# %%
quebecCityPermits.to_csv("./data/quebecCityPermits.csv", index=False)

# %%
