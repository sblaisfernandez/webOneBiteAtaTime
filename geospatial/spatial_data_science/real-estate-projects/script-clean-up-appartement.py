# %%
import geopandas as gpd
import pandas as pd
from shapely.geometry.base import BaseGeometry
import requests
from io import StringIO
import uuid

# %%
logisQuebecAppartements = gpd.read_file(
    "./data/20250518-logisquebec-appartements.geojson"
)

# %%
# Map over each row of logisQuebecAppartements then divide value of the position in the geometry column by 1000000
logisQuebecAppartements["geometry"] = logisQuebecAppartements.geometry.apply(
    lambda point: point.__class__(point.x / 100000, point.y / 100000)
)
# %%
logisQuebecAppartements.head()


# %%

# %%
# Create a new dataframe name appartements from the columns id, adresse, piece, chambre_coucher,superficie, ville_ville, _short_description, _prix_demande, geometry
appartements = logisQuebecAppartements[
    [
        "id",
        "adresse",
        "piece",
        "chambre_coucher",
        "superficie",
        "ville_ville",
        "_short_description",
        "_prix_demande",
        "_url" "geometry",
    ]
].copy()

# %%
#  Convert the name of the columns to addresse to address
appartements.rename(
    columns={
        "adresse": "address",
        "piece": "number_of_rooms",
        "chambre_coucher": "number_of_bedrooms",
        "superficie": "area",
        "ville_ville": "city",
        "_short_description": "description",
        "_prix_demande": "price",
        "source_url": "_url",
    },
    inplace=True,
)

# %%
appartements.head()

# %%
# Save dataframe to CSV file
appartements.to_csv(
    "./data/20250518-logisquebec-appartements-clean.csv", index=False, encoding="utf-8"
)

# %%

# %%
