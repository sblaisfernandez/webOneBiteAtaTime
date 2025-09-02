# %%
from dotenv import find_dotenv, load_dotenv
from supabase import create_client, Client
import geopandas as gpd
import os
import pandas as pd

from quebecCityPermitsConfiguration import (
    quebecCityPermitsColumns,
)

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
print(response.data)


# %%
# Create a new table permits
try:
    response = (
        supabase.table("permits")
        .create(
            {
                "id": "uuid",
                quebecCityPermitsColumns["NUMERO_PERMIS"]: "date",
                quebecCityPermitsColumns["DATE_DELIVRANCE"]: "text",
                quebecCityPermitsColumns["ADRESSE_TRAVAUX"]: "text",
                quebecCityPermitsColumns["DOMAINE"]: "text",
                quebecCityPermitsColumns["LOTS_IMPACTES"]: "text",
                quebecCityPermitsColumns["TYPE_PERMIS"]: "text",
                quebecCityPermitsColumns["RAISON"]: "text",
                quebecCityPermitsColumns["ARRONDISSEMENT"]: "text",
                quebecCityPermitsColumns["GEOMETRY"]: "geometry",
            }
        )
        .execute()
    )
    print("Table 'permits' created successfully.")
    print(response.data)
except Exception as e:
    print(f"Error creating table: {e}")

# %%

# %%
# Generate SQL script that create a table permits
create_table_sql = """
CREATE TABLE IF NOT EXISTS permits (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    PERMIT_NUMBER TEXT,
    ISSUE_DATE DATE,
    WORK_ADDRESS TEXT,
    DOMAIN TEXT,
    AFFECTED_LOTS TEXT,
    PERMIT_TYPE TEXT,
    REASON TEXT,
    BOROUGH TEXT,
    GEOMETRY GEOMETRY
);
"""
