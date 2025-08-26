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
from folium.plugins import MarkerCluster
from bs4 import BeautifulSoup
from typing import List
from shapely.geometry.base import BaseGeometry


def getProvince(electoralDistrict: str) -> str:
    electoralDistrictDictionary = {
        10: "Newfoundland and Labrador",
        11: "Prince Edward Island",
        12: "Nova Scotia",
        13: "New Brunswick",
        24: "Quebec",
        35: "Ontario",
        46: "Manitoba",
        47: "Saskatchewan",
        48: "Alberta",
        59: "British Columbia",
        60: "Yukon",
        61: "Northwest Territories",
        62: "Nunavut",
    }
    province = "n.a."
    electoralDistrictCode = int(electoralDistrict[0:2])

    if electoralDistrictCode in electoralDistrictDictionary:
        province = electoralDistrictDictionary[electoralDistrictCode]

    return province


# %%
candidates = gpd.read_file("Candidats.csv", sep=",")
electoralDistrict = gpd.read_file("CF_CA_2023_FR.geojson", sep=",")


# %%
electoralDistrict.head()


# %%
# Check if all geometries are valid Shapely objects
is_shapely = electoralDistrict["geometry"].apply(lambda x: isinstance(x, BaseGeometry))
# Print rows with invalid geometries
invalid_geometries = electoralDistrict[~is_shapely]
print(invalid_geometries)


# %%
# Check for invalid geometries
invalid_geometries = electoralDistrict[~electoralDistrict["geometry"].is_valid]
print(invalid_geometries)


# %%
# set the precision of the geometry to 6 decimal places
electoralDistrict["geometry"] = electoralDistrict["geometry"].apply(
    lambda x: x.set_precision(6)
)


# %%
candidates["Province"] = candidates[
    "Electoral District Number / No de circonscription"
].apply(lambda x: getProvince(str(x)[0:2]))

# Clean up data
electorDistrictCodeAndName = candidates[
    [
        "Electoral District Number / No de circonscription",
        "Electoral District Name",
        "Nom de la circonscription",
        "Province",
        "Appartenance politique",
        "Candidate's Family Name / Nom de famille du candidat",
        "Candidate's First Name / Prénom du candidat",
    ]
]
electoralDistrictCodeAndName = electorDistrictCodeAndName.rename(
    columns={"Electoral District Number / No de circonscription": "ED code"}
)
electoralDistrict = electoralDistrict.drop(columns=["description", "doc_name"])
electoralDistrict = electoralDistrict.rename(
    columns={"name": "Electoral District Name"}
)

# Merge the two DataFrames on the matching column
mergedElectoralDistrict = electoralDistrict.merge(
    electoralDistrictCodeAndName,
    left_on="Electoral District Name",  # Column in electoralDistrict
    right_on="Electoral District Name",  # Column in electoralDistrictCodeAndName
    how="left",  # Use 'left' to keep all rows from electoralDistrict
)

# %%
# Reorder columns
mergedElectoralDistrict = mergedElectoralDistrict[
    [
        "ED code",
        "Electoral District Name",
        "Nom de la circonscription",
        "Province",
        "Appartenance politique",
        "Candidate's Family Name / Nom de famille du candidat",
        "Candidate's First Name / Prénom du candidat",
        "geometry",
    ]
]

# %% Merge 3 string columns into 1 string
mergedElectoralDistrict = mergedElectoralDistrict.assign(
    CandidatesAndParty=mergedElectoralDistrict.apply(
        lambda x: f"{x['Candidate\'s First Name / Prénom du candidat']} {x['Candidate\'s Family Name / Nom de famille du candidat']} du {x['Appartenance politique']}",
        axis=1,
    )
)

mergedElectoralDistrict = mergedElectoralDistrict.drop(
    columns=[
        "Nom de la circonscription",
        "Appartenance politique",
        "Candidate's Family Name / Nom de famille du candidat",
        "Candidate's First Name / Prénom du candidat",
    ]
)
mergedElectoralDistrict = mergedElectoralDistrict[
    [
        "ED code",
        "Electoral District Name",
        "Province",
        "CandidatesAndParty",
        "geometry",
    ]
]

# %%
# Group by the ED code then concat value in the column  CandidatesAndParty
mergedElectoralDistrict = (
    mergedElectoralDistrict.groupby(["ED code", "Electoral District Name", "Province"])
    .agg(
        {
            "CandidatesAndParty": lambda x: " / ".join(x),
            "geometry": "first",
        }
    )
    .reset_index()
)

# %%
# Create a subset of the mergedLElectoralDistrict  only for the province of Quebec
mergedElectoralDistrictQuebec = mergedElectoralDistrict[
    mergedElectoralDistrict["Province"] == "Quebec"
]
mergedElectoralDistrictQuebec.to_csv(
    "electoralDistrictGroupByEDCodeQuebec.csv", index=False, sep=";"
)

# %%
# Set precision of the geometry to 6 decimal places
mergedElectoralDistrictQuebec["geometry"] = mergedElectoralDistrictQuebec[
    "geometry"
].apply(lambda x: x.set_precision(6))


# %%
mergedElectoralDistrictQuebec.head(10)


# --- Final ---

# %%
# mergedElectoralDistrict.to_csv("electoralDistrictGroupByEDCode.csv", index=False)

# %%
