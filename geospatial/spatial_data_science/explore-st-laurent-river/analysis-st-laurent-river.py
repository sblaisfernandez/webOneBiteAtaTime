
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

dataFolderRelativePath = './data'

# %%
## DataSources
adminBoundariesUrl = 'https://diffusion.mern.gouv.qc.ca/Diffusion/RGQ/Vectoriel/Theme/Local/SDA_20k/FGDB/SDA.gdb.zip'

# Répertoire des municipalités du Québec
# https://www.donneesquebec.ca/recherche/dataset/repertoire-des-municipalites-du-quebec
municipalities_CsvUrl = 'https://donneesouvertes.affmunqc.net/repertoire/MUN.csv'
MRC_CsvUrl = 'https://donneesouvertes.affmunqc.net/repertoire/MRC_CM_Arg.csv'
# The column 'mcode' of municipalities match with 'MUS_CO_GEO' of municipalitiesBoundaries


# Géobase du réseau hydrographique du Québec (GRHQ)
# https://www.donneesquebec.ca/recherche/dataset/grhq
grhqUrl = 'https://diffusion.mern.gouv.qc.ca/Diffusion/RGQ/Vectoriel/Carte_Topo/Local/GRHQ/FGDB/00/00.zip'

# Caractérisation des berges de la partie fluviale du Saint-Laurent et analyse de l'évolution des facteurs hydro-climatiques influençant les aléas d'érosion et d'inondation
# https://catalogue.ogsl.ca/fr/dataset/ca-cioos_448d2828-d249-4d77-ad68-563512977150
riverLineUrl = 'https://catalogue.ogsl.ca/data/melcc/ca-cioos_448d2828-d249-4d77-ad68-563512977150/CaractBerges_TCREF_UL_Mars2020.zip'

# Modèles numériques de terrain hydro cohérents à l’échelle régionale
# https://www.donneesquebec.ca/recherche/dataset/modeles-numerique-de-terrain-hydro-coherents-a-l-echelle-regionale
mntHydroUrl = ''

#### Water flood
floodingUrl = 'https://www.donneesquebec.ca/recherche/dataset/cartographie-des-inondations-du-printemps-2023'


# %%
response = requests.get(adminBoundariesUrl)
response.raise_for_status()
zip_file = zipfile.ZipFile(io.BytesIO(response.content))
zip_file.extractall(path=dataFolderRelativePath)
adminBoundariesPath = dataFolderRelativePath + '/SDA.gdb'
# layers = fiona.listlayers(adminBoundariesPath)
municipalitiesBoundaries = gpd.read_file(adminBoundariesPath, layer='munic_s')
municipalitiesBoundaries.to_csv(f'{dataFolderRelativePath}/municipalitiesBoundaries.csv', index=False)
# municipalitiesBoundaries.plot()
# municipalitiesBoundaries.crs

# %%
st_Lawrence_river_overlap_path = f'{dataFolderRelativePath}/st-lawrence-river-overlap.json'
st_LawrenceRiverOverlap = gpd.read_file(st_Lawrence_river_overlap_path)
st_LawrenceRiverOverlap

# Create a new GeoDataFrame with the merged polygon
st_LawrenceRiverOverlap = gpd.GeoDataFrame(geometry=[st_LawrenceRiverOverlap.unary_union])
# Save the merged GeoDataFrame to a new file
st_LawrenceRiverOverlap.to_file(f'{dataFolderRelativePath}/merged_st_lawrence_river_overlap.json', driver='GeoJSON')
st_LawrenceRiverOverlap.set_crs(epsg=4326, inplace=True)
st_LawrenceRiverOverlap = st_LawrenceRiverOverlap.to_crs(epsg=4269)
st_LawrenceRiverOverlap.crs
st_LawrenceRiverOverlap.plot()

# %%
response = requests.get(MRC_CsvUrl)
response.raise_for_status()
csv_data = StringIO(response.text)
mrc = pd.read_csv(csv_data)

# %%
response = requests.get(municipalities_CsvUrl)
response.raise_for_status()
csv_data = StringIO(response.text)
municipalitiesRaw = pd.read_csv(csv_data)
municipalitiesRaw['mcode'] = municipalitiesRaw['mcode'].astype(int)

response = requests.get(MRC_CsvUrl)
response.raise_for_status()
csv_data = StringIO(response.text)
mrc = pd.read_csv(csv_data)

# %%
# response = requests.get(grhqUrl)
# response.raise_for_status()
# zip_file = zipfile.ZipFile(io.BytesIO(response.content))
# zip_file.extractall(path=dataFolderRelativePath)


# %%
# Create a new DataFrame from all the polygon of municipalitiesBoundaries that are overlap by the st_LawrenceRiverOverlap dataFrame
costalMunicipalitiesIntersect = gpd.overlay(municipalitiesBoundaries, st_LawrenceRiverOverlap, how='intersection')
costalMunicipalities =  costalMunicipalitiesIntersect[['MUS_CO_GEO', 'MUS_NM_MUN', 'MUS_NM_NMC', 'MUS_NM_MRC']]
costalMunicipalities = costalMunicipalities.merge(municipalitiesBoundaries, on='MUS_CO_GEO')
costalMunicipalities = costalMunicipalities.rename(columns={'geometry_y':'geometry'})
costalMunicipalities = costalMunicipalities.set_geometry('geometry')
# Export costalMunicipalities to a .CSV
# costalMunicipalities.plot()
costalMunicipalities.rename(columns={'MUS_CO_GEO':'mcode'}, inplace=True)
costalMunicipalities['mcode'] = costalMunicipalities['mcode'].astype(int)
costalMunicipalities = costalMunicipalities[['mcode', 'MUS_NM_MUN', 'MUS_NM_NMC', 'MUS_NM_MRC', 'geometry']]

# %%
# municipalitiesRaw.set_index('mcode', inplace=True)
municipalities = municipalitiesRaw[['mcode', 'munnom', 'madr1', 'mcourriel', 'mweb', 'mtel', 'trvpub', 'mesurg', 'urban']]
municipalities['mcode'] = municipalities['mcode'].astype(int)
# %%
costalMunicipalities = costalMunicipalities.merge(municipalities, on='mcode')
costalMunicipalities = costalMunicipalities[['mcode', 'munnom', 'geometry']]
subSet_costalMunicipalities = costalMunicipalities.head(1)
# %% How to validate the geometry column is valid
is_valid = subSet_costalMunicipalities['geometry'].apply(wkt.loads).apply(lambda x: x.is_valid)
is_valid

type(subSet_costalMunicipalities['geometry'])
geom = subSet_costalMunicipalities['geometry']
geom

# Convert the pandas DataFrame to a GeoPandas GeoDataFrame
subSet_costalMunicipalities_gdf = gpd.GeoDataFrame(subSet_costalMunicipalities, geometry='geometry')

subSet_costalMunicipalities.to_csv(f'{dataFolderRelativePath}/subsetCostalMunicipalities.csv', index=False)

# Geopandas export subSet_costalMunicipalities to a Geojson file
subSet_costalMunicipalities.to_file(f'{dataFolderRelativePath}/subsetCostalMunicipalities.geojson', driver='GeoJSON')

# %%
# Create a folium map centered around the St. Lawrence River
customMap = folium.Map(location=[46.8, -71.2], zoom_start=7)

# Add the costalMunicipalities polygons to the map
for _, row in costalMunicipalities.iterrows():
    sim_geo = gpd.GeoSeries(row['geometry']).simplify(tolerance=0.001)
    geo_json = sim_geo.to_json()
    geo_json_layer = folium.GeoJson(data=geo_json, style_function=lambda x: {'fillColor': 'blue'})
    geo_json_layer.add_to(customMap)

# Save the map to an HTML file
customMap
# %%
