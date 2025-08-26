
# %%
# Create a GeoDataFrame from the WKT string
geometry = wkt.loads('LINESTRING (45.0064051 -74.7950346, 50.3348612 -64.1506207)')
centerLineStLawrenceRiver = gpd.GeoDataFrame([{'geometry': geometry}], crs="EPSG:4326")
centerLineStLawrenceRiver.buffer()



# %%
grhqPath = dataFolderRelativePath + '/GRHQ_00AA.gdb'
grhq_layers = fiona.listlayers(grhqPath)
grhq_layers
RH_R = gpd.read_file(grhqPath, layer='RH_R')

# %%
# Explore RHG_L
RH_R = RH_R.to_crs(epsg=4326)
RH_R.head()
RH_R.describe()
RH_R.plot()
subset_RH_R = RH_R[0:400]
subset_RH_R.plot()

# %%
# Create a Folium map centered around the approximate center of the dataset
customMap = folium.Map(location=[45, -73], zoom_start=10)

# Add the GeoDataFrame to the map
folium.GeoJson(subset_RH_R).add_to(customMap)

customMap

# %%



# %%
# Find string 'Percé' in the column 'munnom' of municipalities
perce_municipalities = municipalities[municipalities['munnom'].str.contains('Percé', case=False, na=False)]
perce_municipalities

# costalMunicipalities = costalMunicipalities[['MUS_CO_GEO', 'MUS_NM_MUN', 'MUS_NM_NMC', 'MUS_NM_MRC', 'geometry']]

costalMunicipalities.rename(columns={'MUS_CO_GEO':'mcode'}, inplace=True)
# Set the geometry column
costalMunicipalities.crs = municipalitiesBoundaries.crs
costalMunicipalities['mcode'] = costalMunicipalities['mcode'].astype(int)
costalMunicipalities.set_index('mcode', inplace=True)
# costalMunicipalities.plot()

costalMunicipalities.head()
costalMunicipalities.mcode.astype(int)

municipalitiesRaw.set_index('mcode', inplace=True)
municipalities = municipalitiesRaw[['mcode', 'munnom', 'madr1', 'mcourriel', 'mweb', 'mtel', 'trvpub', 'mesurg', 'urban']]

municipalities.head(20)
municipalities.describe()
costalMunicipalities.head(20)
costalMunicipalities.describe()

# %%
outPutMunicipalities = costalMunicipalities.merge(municipalities, on='mcode')
outPutMunicipalities

# %%


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
