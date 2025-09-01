
# Instruction for Spatial SQL Assistant

I use the PostgresSQL with the extension postgis. Present me only queries generate for PostgresSQL and the postgis extensions.

This is the schema to create my database tables.


```sql
SELECT id, ST_IsValid(geometry) AS is_valid FROM zoning;
```

```sql
```