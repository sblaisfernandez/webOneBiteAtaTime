
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

dataFolderRelativePath = './data'

# %%
## DataSources
fireStationsUrl = 'https://geoegl.msp.gouv.qc.ca/apis/wss/incendie.fcgi?service=wfs&version=1.1.0&request=getfeature&typename=MSP_CASERNE_PUBLIC&outputformat=CSV'
adminBoundariesUrl = 'https://diffusion.mern.gouv.qc.ca/Diffusion/RGQ/Vectoriel/Theme/Local/SDA_20k/FGDB/SDA.gdb.zip'
quebecBuildingUrl = 'https://www.donneesquebec.ca/recherche/dataset/d2a34f6d-3750-44e9-9a6d-aa9494a34df7/resource/0920b952-b349-4ddd-a7e3-eebf6f6b6336/download/vdq-batiments.csv'

#### Carte de vigilance multirisque-avertissements et alertes d'Environnement et Changement climatique Canada
vigilanceUrl = 'https://www.donneesquebec.ca/recherche/dataset/carte-vigilance-multirisque-meteo-alerte-ec'
#### Événements de sécurité civile
eventsCivilSecurityUrl = 'https://www.donneesquebec.ca/recherche/dataset/evenements-de-securite-civile'
#### Water flood
floodingUrl = 'https://www.donneesquebec.ca/recherche/dataset/cartographie-des-inondations-du-printemps-2023'

# %%
response = requests.get(fireStationsUrl)
response.raise_for_status()
csv_data = StringIO(response.text)
fireStations = pd.read_csv(csv_data)

# %%
fireStations =  gpd.GeoDataFrame(fireStations, geometry=gpd.points_from_xy(fireStations.coord_x, fireStations.coord_y), crs='EPSG:4326')
fireStations.drop(columns=['coord_x', 'coord_y'], inplace=True)
fireStations.head()
fireStations_in_capitalNationale = gpd.sjoin(fireStations, capitalNationale, how="inner", op="within")

# %%
response = requests.get(adminBoundariesUrl)
response.raise_for_status()
zip_file = zipfile.ZipFile(io.BytesIO(response.content))
zip_file.extractall(path=dataFolderRelativePath)

# %%
path = dataFolderRelativePath + '/SDA.gdb'
layers = fiona.listlayers(path)
administrativeRegions = gpd.read_file(path, layer='regio_s')

# %%
capitalNationale = administrativeRegions[administrativeRegions['RES_NM_REG'] == 'Capitale-Nationale']
capitalNationale = capitalNationale.to_crs('EPSG:4326')
capitalNationale

# %%
response = requests.get(quebecBuildingUrl)
response.raise_for_status()
quebecBuildingCsv = StringIO(response.text)
quebecBuilding = pd.read_csv(quebecBuildingCsv)

# %%
quebecBuilding.rename(columns={'ï»¿ID': 'ID'}, inplace=True)

# Create a subset of quebecBuilding with 100 rows
quebecBuilding['SOURCE_CAPTAGE'] = quebecBuilding['SOURCE_CAPTAGE'].str.replace('PhotogrammÃ©trie', 'Photogrammetrie')
quebecBuilding['GEOMETRIE'] = quebecBuilding['GEOMETRIE'].apply(wkt.loads)
quebecBuilding = gpd.GeoDataFrame(quebecBuilding, geometry='GEOMETRIE')
quebecBuilding_subset = quebecBuilding.head(1000)

# %%
# Create a base map
customMap = folium.Map(location=[46.8, -71.2], zoom_start=11, titles='Stamen Terrain')

# Create the folium layer
layerCapitalNational = folium.GeoJson(
    capitalNationale,
    name='Capital Nationale',
    style_function=lambda x: {'fillColor': 'green', 'color': 'black', 'weight': 1, 'fillOpacity': 0.1}
)

# Add fire stations markers
marker_cluster = MarkerCluster().add_to(customMap)
for idx, row in fireStations_in_capitalNationale.iterrows():
    folium.Marker(
        location=[row.geometry.y, row.geometry.x],
        popup=row['adresse'],
        icon=folium.Icon(color='red', icon='fire', prefix='fa')
    ).add_to(marker_cluster)

for id, row in quebecBuilding_subset.iterrows():
    building = gpd.GeoSeries(row["GEOMETRIE"])
    building_json = building.to_json()
    building_json = folium.GeoJson(data=building_json, style_function=lambda x: {"fillColor": "orange"})
    building_json.add_to(customMap)
    # folium.Popup(row["TYPE_BATIMENT"]).add_to(building_json)

layerCapitalNational.add_to(customMap)
folium.LayerControl().add_to(customMap)

customMap
