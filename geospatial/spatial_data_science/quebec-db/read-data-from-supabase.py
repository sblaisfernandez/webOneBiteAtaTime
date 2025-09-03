# %%
from dotenv import find_dotenv, load_dotenv
from supabase import create_client, Client
import geopandas as gpd
import os
import pandas as pd

from quebecCityPermitsConfiguration import mySupabase

load_dotenv(dotenv_path="/Users/blais/nplus1/webOneBiteAtaTime/.env")

supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_ANON_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

# %%
try:
    response = supabase.table("test").select("*").execute()
    print(response.data)
except Exception as e:
    print(f"Error inserting data: {e}")

# %%
try:
    response = supabase.table("quebec_city_permits").select("*").execute()
    print(response.data)
except Exception as e:
    print(f"Error reading data: {e}")

# %%

# %%
