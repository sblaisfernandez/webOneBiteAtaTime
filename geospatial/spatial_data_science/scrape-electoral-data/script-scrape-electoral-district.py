#%%
import geopandas as gdf
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

## DataSources
baseUrlElectionCanada = 'https://www.elections.ca/content.aspx?section=res&dir=cir/red/343list&document=index&lang=e'

#%%
# Create a geodataframe with the columns ED code, province, Federal Electoral Districts,
electoralDistrictHeaders = ['ED code', 'Province', 'Federal Electoral Districts']
electoralDistrict = gdf.GeoDataFrame(columns=electoralDistrictHeaders)

# %%
response = requests.get(baseUrlElectionCanada)
response.raise_for_status()
html_data = response.text
soup = BeautifulSoup(html_data, 'html.parser')
# find all the table with the class="widthFull tableau"
tables = soup.find_all('table', class_='widthFull tableau')

# %%
def getProvince(electoralDistrict: str) -> str:
    electoralDistrictDictionary = {
        10: 'Newfoundland and Labrador',
        11: 'Prince Edward Island',
        12: 'Nova Scotia',
        13: 'New Brunswick',
        24: 'Quebec',
        35: 'Ontario',
        46: 'Manitoba',
        47: 'Saskatchewan',
        48: 'Alberta',
        59: 'British Columbia',
        60: 'Yukon',
        61: 'Northwest Territories',
        62: 'Nunavut'
    }
    province = 'n.a.'
    electoralDistrictCode = int(electoralDistrict[0:2])

    if electoralDistrictCode in electoralDistrictDictionary:
        province = electoralDistrictDictionary[electoralDistrictCode]

    return province

# %%
# loop over each tr of table then extract the td elements
for table in tables:
    rows = table.find_all('tr')
    for row in rows:
        # Extract the td elements from the row
        currentRow = row.find_all('td')
        # Extract the text from each td element
        data = [column.get_text(strip=True) for column in currentRow]
        if len(data) >= 2:
            new_row = {electoralDistrictHeaders[0]: data[0], electoralDistrictHeaders[1]: getProvince(data[0]),  electoralDistrictHeaders[2]: data[1]}
            electoralDistrict.loc[len(electoralDistrict)] = new_row

# %%
# electoralDistrict.describe()
electoralDistrict.head(30)

# %% output the electoralDistrict to a csv file
electoralDistrict.to_csv('electoral-district.csv', index=False)