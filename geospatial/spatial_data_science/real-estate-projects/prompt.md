
# Prompt for chatGPT

Ton rôle est d'être un analyse de marché Immobilier spécialisé un appartement dans le marché de Québec au Canada en 2025.

T'attache et de lire des pages Web, puis d'agréger l'information pour faire l'analyse.

Ta mission est de récupérer les données à partir des différents sites Web.

## Registre des loyers

```bash
curl 'https://registre-des-loyers.ca/api/v1/housings/46.89406948944127,-71.22531124237905,46.876118868578644,-71.27374120835195' \
  -H 'accept: */*' \
  -H 'accept-language: en-US,en;q=0.5' \
  -b 'aaa=10; october_session=eyJpdiI6IlRTWHozR1J1V3RLcm8yaGxFTFhNRWc9PSIsInZhbHVlIjoiRHVPZTJ5U0NVaE9oNFwvSUt2RjAyU3R1VE9lQ2FBa2xaMWh2YWdoRHhudWtpQzZjbm1vMWhoNWdQV1grYXc4MGVkajVlRlVzWGVFZzUxYnZZQXdMT1J2bklRQ0J4RXF4ZFRHYlFcL3BNc0tmNFZ1M1ptQkR2T0xcLzdKSURjQXpha0MiLCJtYWMiOiI1YWQxZTg1MjVhZmMyMDk5ZjU5MjZjNGIxODY0MjVlZDQ5ODk4YjE4NzM0YTdjMjkyMmE4YjdmNDkxYzczNThkIn0%3D' \
  -H 'priority: u=1, i' \
  -H 'referer: https://registre-des-loyers.ca/fr/qc/carte/' \
  -H 'sec-ch-ua: "Chromium";v="136", "Brave";v="136", "Not.A/Brand";v="99"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "macOS"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-origin' \
  -H 'sec-gpc: 1' \
  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36'
```

## SCHL - Portail de l’information sur le marché de l’habitation*

<https://www03.cmhc-schl.gc.ca/hmip-pimh/fr#Profile/1400/3/Qu%C3%A9bec>

## Logis Quebec

Lis l'URL suivante:<https://www.logisquebec.com/result-search.php?tri=2&source=a_louer&type=1&region=13&ville=1851&prix_min=0&prix_max=999999999&room=&from_search=true&from_filter=true>

Puis récupère l'information dans un format CSV suivant:

Adresse, quartier, montant du loyer, nombre de chambres, nombre de salles de bain, taille de l'appartement, type de stationnement, inclusions, charge du locataire, autre.

NOT WORKING BLOCK BY GPT
---

## Kangaloo

Lis l'URL suivante:<https://www.logisquebec.com/result-search.php?tri=2&source=a_louer&type=1&region=13&ville=1851&prix_min=0&prix_max=999999999&room=&from_search=true&from_filter=true>

Puis récupère l'information dans un format CSV suivant:

Adresse, quartier, montant du loyer, nombre de chambres, nombre de salles de bain, taille de l'appartement, type de stationnement, inclusions, charge du locataire, autre.

NOT WORKING BLOCK BY GPT

## Lespacs

Lis l'URL suivante:<https://www.lespac.com/quebec/immobilier-location-logements_b457g15398k1R2.jsa>

Puis récupère l'information dans un format CSV suivant:

Adresse, quartier, montant du loyer, nombre de chambres, nombre de salles de bain, taille de l'appartement, type de stationnement, inclusions, charge du locataire, autre.

NOT WORKING BLOCK BY GPT
