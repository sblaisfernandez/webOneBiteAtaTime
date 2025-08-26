# Learn PostGIS

Create the docker container.

POSTGRES_USER=postgres
POSTGRES_DB=postgres

```bash
docker run -p 5432:5432 --name mydb -e POSTGRES_PASSWORD=mypassword -d postgis/postgis
```

## Connect to the database

F1 -> Database Client: Add Connection
