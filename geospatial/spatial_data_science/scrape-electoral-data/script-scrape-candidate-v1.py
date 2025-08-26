#%%
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

# %%
politicalParty = [ 'Bloc Québécois / Bloc Québécois', 'Parti conservateur du Canada / Conservative Party of Canada', 'Parti libéral du Canada / Liberal Party of Canada', 'Nouveau Parti démocratique / New Democratic Party', 'Parti Rhinocéros Party / Parti Rhinocéros Party' ]


# %%
# Read data from  the CSV file
electoralDistrictCode = pd.read_csv('electoral-district.csv')
electoralDistrictCode.head(50)
# Create a subset of  electoralDistrictCode only for the province of quebec
electoralDistrictQuebec = electoralDistrictCode[electoralDistrictCode['Province'] == 'Quebec']
# get the first 10 Electoral Districts of Quebec
electoralDistrictQuebec = electoralDistrictQuebec.head(10)

# %%
# Group rows by province and count the number of occurrences
def getElectionCanadaWebpage(idElectoralDistrict: str) -> str:
    baseUrlElectionCanada = 'https://www.elections.ca/Scripts/vis/Candidates/Print?L=f&ED={{idElectoralDistrict}}}&EV=62&EV_TYPE=1&PROV=QC&PROVID=24&QID=-1&PAGEID=17'
    electionCanadaUrl = baseUrlElectionCanada.replace('{{idElectoralDistrict}}', idElectoralDistrict)

    response = requests.get(electionCanadaUrl)
    response.raise_for_status()
    html_data = response.text
    soup = BeautifulSoup(html_data, 'html.parser')
    candidateTables = soup.find('ul', class_='multicol')

    return candidateTables


def getCandidateList(candidateTables):
    # Loop over each li of the ul element then extract raw html element of  li element
    candidateList = []
    for li in candidateTables.find_all('li'):
        # Extract the text from the li element
        candidate = li.get_text(strip=False)
        candidate = candidate.replace('\r\n', ';')
        # convert string candidate to list of rows
        candidate = candidate.split(';')
        # loop over each item in candidate list then trim space at the beginning and end of the string
        candidate = [item.strip() for item in candidate]
        # remove empty string from candidate list
        candidate = list(filter(None, candidate))
        # print('*** starting printing li ***')
        candidateList.append(candidate)

    return candidateList

#%%
# main script
candidateTables = getElectionCanadaWebpage('24001')
candidateList = getCandidateList(candidateTables)
print(candidateList)

# %%
# Loop over each candidate in electoralDistrictQuebec then add candidate and political party to the row of electoralDistrictQuebec
electoralDistrictQuebec['Political Party'] = ''


electoralDistrictQuebec.head()




# %%
for index, row in electoralDistrictQuebec.iterrows():
    # Get the candidate list for the current electoral district
    candidateTables = getElectionCanadaWebpage(row['Electoral District Code'])
    candidateList = getCandidateList(candidateTables)
    # Loop over each candidate in the candidate list then add candidate and political party to the row of electoralDistrictQuebec
    for candidate in candidateList:
        if len(candidate) > 1:
            electoralDistrictQuebec.at[index, 'Political Party'] = candidate[1]
        else:
            electoralDistrictQuebec.at[index, 'Political Party'] = 'n.a.'

