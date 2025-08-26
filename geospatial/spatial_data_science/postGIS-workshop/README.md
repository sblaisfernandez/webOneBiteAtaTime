# WORKSHOP LEARN POSTGIS FAST

- [PostGIS Workshop](https://docs.google.com/presentation/d/1tOrp4MQebozybREHYDlE2ZQRlM9Dkne-nRMyCRWc6KY/edit#slide=id.gdd2fd99493_0_607)
- [PostGIS Intro](https://postgis.net/workshops/postgis-intro/introduction.html)
- [PostGIS Baby Steps](https://www.youtube.com/playlist?list=PLj5uPTt8jS8zzXfWvtqaT8pYhKWnPRFox)

## Learn Spatial SQL

[PostGIS follows the OGC/SQL-MM standards.](https://postgis.net/docs/manual-dev/using_postgis_dbmanagement.html#RefObject)

[CrunchyData](https://www.crunchydata.com/developers/tutorials)

## postGIS workshop

```bash
docker run --name=workshopDB -d -e POSTGRES_USER=workshopDB -e POSTGRES_PASS=workshopDB -e POSTGRES_DBNAME=workshopDB -p 5432:5432 --restart=always mdillon/postgis
```

### Learning source

<https://postgis.net/documentation/training/>

<https://www.naturalearthdata.com/>

### Créer les extensions nécessaire sur la bd PostgresSQL locale

Il faut créer les extensions suivantes (Vous pouvez exécuter les commandes dans un client BD tel que DBeaver):

```sql
CREATE EXTENSION IF NOT EXISTS unaccent;

CREATE EXTENSION IF NOT EXISTS pg_trgm;
```

### Importing data into the workshop

```bash
$ cd workshop/postgis-workshop/data/2000

ogr2ogr \
    -nln nyc_census_blocks_2000 \
    -nlt PROMOTE_TO_MULTI \
    -lco GEOMETRY_NAME=geom \
    -lco FID=gid \
    -lco PRECISION=NO \
    Pg:'dbname=workshop host=localhost user=workshop port=5432' \
    nyc_census_blocks_2000.shp
```

```bash
$ conda install -c conda-forge shp2pgsql

shp2pgsql \
    -D \
    -I \
    -s 26918 \
    nyc_census_blocks_2000.shp \
    nyc_census_blocks_2000 \
    | dbname=workshop host=localhost user=workshop
```
