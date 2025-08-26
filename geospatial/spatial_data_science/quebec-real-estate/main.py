# %%
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import fiona
from shapely import wkt
from sqlalchemy import create_engine
import requests, zipfile, io
from io import StringIO
import folium
import os
from supabase import create_client, Client


# %%
supabase_url = "https://krnhjtghvzbzptvoddxn.supabase.co"
supabase_key = ""
url: str = os.environ.get(supabase_url)
key: str = os.environ.get(supasbase_key)


supabase: Client = create_client(url, key)
