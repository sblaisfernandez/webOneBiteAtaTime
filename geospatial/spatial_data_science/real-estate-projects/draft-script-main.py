# %%
import geopandas as gpd
import pandas as pd
from shapely.geometry.base import BaseGeometry
import requests
from io import StringIO
import uuid

arrondissements = "https://www.donneesquebec.ca/recherche/dataset/5ddf584d-b73d-4cd7-b203-28c3b5364d66/resource/99b654d9-089e-4503-8508-fc184368f8af/download/vdq-arrondissement.csv"

# %%
quebecProjectsCSV = pd.read_csv("data/quebec-real-estate-projects.csv", sep=",")
affectationSolCsv = pd.read_csv("data/vdq-schemagrandeaffectation.csv")

# %%
try:
    response = requests.get(arrondissements)
    response.raise_for_status()

    if response.encoding != "utf-8":
        response.encoding = "utf-8"

    text = response.text

except requests.exceptions.RequestException as e:
    print(f"Request error: {e}")
except UnicodeDecodeError as e:
    print(f"Decoding error: {e}. Try a different encoding.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

# %%
csv_data = StringIO(text)
boroughs = pd.read_csv(csv_data)
boroughsWKF = gpd.GeoSeries.from_wkt(boroughs["GEOMETRIE"], crs="EPSG:4326")

# %%

# %%
# Convert boroughs to a GeoDataFrame
boroughs = gpd.GeoDataFrame(
    boroughs,
    geometry=boroughsWKF,
    crs="EPSG:4326",
)

# %%
geometrie = gpd.GeoSeries.from_wkt(affectationSolCsv["GEOMETRIE"], crs="EPSG:4326")

# %%
# Generate a uuid() for each row in  quebecProjectsCSV
quebecProjectsCSV["Id"] = quebecProjectsCSV.apply(lambda x: uuid.uuid4(), axis=1)
wkf = gpd.GeoSeries.from_wkt(quebecProjectsCSV["wkf"], crs="EPSG:4326")

# %%
quebecProjects = gpd.GeoDataFrame(
    {
        "Id": quebecProjectsCSV["Id"],
        "Arrondissement": quebecProjectsCSV["Arrondissement"],
        "Date": quebecProjectsCSV["Date"],
        "Nom": quebecProjectsCSV["Nom"],
        "Nombre de logements": quebecProjectsCSV["Nombre de logements"],
        "Type": quebecProjectsCSV["Type"],
        "Promoteur": quebecProjectsCSV["Promoteur"],
        "Téléphone": quebecProjectsCSV["Téléphone"],
        "url": quebecProjectsCSV["url"],
        "geometry": wkf,
    },
    crs="EPSG:4326",
)

# %%
affectationSol = gpd.GeoDataFrame(
    {
        "ID": affectationSolCsv["ID"],
        "CODE_AFFECTATION": affectationSolCsv["CODE_AFFECTATION"],
        "AFFECTATION": affectationSolCsv["AFFECTATION"],
        "NO_REGLEMENT": affectationSolCsv["NO_REGLEMENT"],
        "STATUT": affectationSolCsv["STATUT"],
        "DATE_VIGUEUR": affectationSolCsv["DATE_VIGUEUR"],
        "geometry": geometrie,
    },
    crs="EPSG:4326",
)

# %%
# Safe quebecProjects to .csv
quebecProjects.to_csv("quebec-real-estate-projects-formatted.csv", index=False)


# %%
boroughs.explore(
    column="NOM",
    tooltip="NOM",
    popup=True,
    tiles="CartoDB positron",
    name="NOMs",
)

# %%

# %%
quebecProjects.explore(
    column="Nom", tooltip="Nom", popup=True, tiles="CartoDB positron"
)


# %%
affectationSol.explore(
    column="AFFECTATION",
    tooltip="AFFECTATION",
    popup=True,
    tiles="CartoDB positron",
    name="affectationSol",
)

# %%

# %%
