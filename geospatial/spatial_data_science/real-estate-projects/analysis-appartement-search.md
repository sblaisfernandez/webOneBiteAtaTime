
# Real Estate Analysis Quebec

Le but de cette analyse et de déterminer un ensemble de terrain sur le territoire de la communauté métropolitaine de Québec avec un potentiel de développement de multi logements.

Le but de l'exercice et de déverser les données vers une base de données supabase Afin de bénéficier du Storage des données dans une base de données relationnelles, afin de bénéficier des fonctions spatiales de l'extension, postGIS.

## Cool tricks to build

- Appartement market watcher ( monitor the number of appartement display on major site)
-

## Search in Kangalou

Get data for the entire province of Quebec from the Kangalou server.

```bash
curl 'https://www.kangalou.com/fr/recherche/ajax/search-map/' \
  -H 'accept: application/json, text/javascript, */*; q=0.01' \
  -H 'accept-language: en-US,en;q=0.8' \
  -H 'content-type: application/x-www-form-urlencoded; charset=UTF-8' \
  -b 'PHPSESSID=d2ner1skcm7p8tccsnkt94chig; _adstanding_local_id=0e0371edab948039924cfddb54026b4c; kgou-search-cts=; kgou-search-lid=; kgou-search-st=' \
  -H 'origin: https://www.kangalou.com' \
  -H 'priority: u=1, i' \
  -H 'referer: https://www.kangalou.com/fr/recherche/?page=1&q=NZA7CsMwEERPY9XSfmSpUBNykWBcpIgJOJCQ0yfeGTeCx452HrtMfsmTX4eIpuUP5YCiNgcJSCVIg7oFGEaOb85gCapBlpGcOUOygaQFdc4yyjOXEinTUF9oYw5UIloKhawDaWQVWLkZgoVOwjClnEWd/igSWjXe5DyRpu95vfR83LfjvX1G2se2vtf99QM%3D' \
  -H 'sec-ch-ua: "Chromium";v="136", "Brave";v="136", "Not.A/Brand";v="99"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "macOS"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-origin' \
  -H 'sec-gpc: 1' \
  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36' \
  -H 'x-requested-with: XMLHttpRequest' \
  --data-raw 'c%5B%5D=223&c%5B%5D=1347&c%5B%5D=1332&c%5B%5D=194&c%5B%5D=1353&c%5B%5D=1331&c%5B%5D=1404&c%5B%5D=1333&c%5B%5D=1328&c%5B%5D=1330&c%5B%5D=1350&c%5B%5D=1382&c%5B%5D=1345&c%5B%5D=1344&c%5B%5D=1349&c%5B%5D=1346&c%5B%5D=1351&c%5B%5D=1329&c%5B%5D=1352&c%5B%5D=1405&c%5B%5D=1387&c%5B%5D=1343&z%5B%5D=&pmin=&pmax=&s=newest&pinsOnly=true'
```

## LogisQuébec

Get all appartement for Quebec city

```bash
curl ' https://www.logisquebec.com/logement-search.php?page=1&config=map&prix_max=999999999&source=a_louer&region=13&type=1&ville=1851&tri=1&bbox=-7963286.043777949%2C5895091.150951793%2C-7917118.078693703%2C5940609.401295614' \
  -H 'accept: */*' \
  -H 'accept-language: en-US,en;q=0.9' \
  -b 'lq_session=048496f9a33cd85bc31a34d58fed00d4; PHPSESSID=vudnvhlal1bi6d059ncv3odavs; source=a_louer; autosuggest=Qu%C3%A9bec%3B13%3B1851; _pubcid=4a526cb7-ac81-4730-8f82-a4699b5f26bb; _pubcid_cst=zix7LPQsHA%3D%3D; lastsearch=https://www.logisquebec.com/map.php?source=a_louer&type=1&region=13&ville=1851&prix_min=0&prix_max=999999999&room=&tri=1&query=Qu%C3%A9bec#x=-7940196&y=5917863&z=12' \
  -H 'priority: u=1, i' \
  -H 'referer: https://www.logisquebec.com/map.php?source=a_louer&type=1&region=13&ville=1851&prix_min=0&prix_max=999999999&room=&tri=1&query=Qu%C3%A9bec' \
  -H 'sec-ch-ua: "Chromium";v="136", "Brave";v="136", "Not.A/Brand";v="99"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "macOS"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-origin' \
  -H 'sec-gpc: 1' \
  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36' \
  -H 'x-requested-with: XMLHttpRequest'
```

## Source of the 18 projects back by the City of Quebec

- [Journal de Quebec](https://www.journaldequebec.com/2025/05/20/construction-de-logements-la-ville-autorisera-2850-nouvelles-unites)
