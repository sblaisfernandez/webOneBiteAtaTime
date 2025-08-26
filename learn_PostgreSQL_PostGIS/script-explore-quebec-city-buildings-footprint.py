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


# [Empreintes des bâtiments de la ville de Québec](<https://www.donneesquebec.ca/recherche/dataset/empreintes-des-batiments/resource/0920b952-b349-4ddd-a7e3-eebf6f6b6336>)


# %%
supabase_url = "https://krnhjtghvzbzptvoddxn.supabase.co"
supabase_key = ""
url: str = os.environ.get(supabase_url)
key: str = os.environ.get(supasbase_key)


supabase: Client = create_client(url, key)
