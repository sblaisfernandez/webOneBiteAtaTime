# %%
import geopandas as gpd
import pandas as pd
from shapely.geometry.base import BaseGeometry
from supabase import create_client, Client
from dotenv import find_dotenv, load_dotenv
import os

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
response = (
    supabase.table("test-table")
    .insert({"id": 2, "created_at": "2025-05-19 20:52:13+00", "name": "Pluto"})
    .execute()
)
print(response)

# %%
try:
    response = supabase.table("projects").select("*").execute()
    print(response)
except Exception as e:
    print(f"Error deleting record: {e}")
