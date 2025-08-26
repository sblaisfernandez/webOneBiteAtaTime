# Postgres Cheat Sheet

This is a collection of the most common commands I run while administering Postgres databases. The variables shown between the open and closed tags, "<" and ">", should be replaced with a name you choose. Postgres has multiple shortcut functions, starting with a forward slash, "\". Any SQL command that is not a shortcut, must end with a semicolon, ";". You can use the keyboard UP and DOWN keys to scroll the history of previous commands you've run.

## Install in Docker for macOS

```bash
docker pull postgis/postgis

docker run --platform linux/arm64 postgis/postgis

docker volume create my-postgis-volume

docker run --name my-postgis-container -e POSTGRES_PASSWORD=password -d postgis/postgis
```

## Data Types

| Category        | Name                      | SQL Symbol                         | Aliases                                   | Description                                | Example                                  |
|----------------|---------------------------|-------------------------------------|-------------------------------------------|--------------------------------------------|-------------------------------------------|
| **Numeric**     | smallint                  | `smallint`                          | `int2`                                     | 2‑byte signed integer                       | `-32768`                                  |
|                | integer                   | `integer`                           | `int`, `int4`                              | 4‑byte signed integer                       | `42`                                      |
|                | bigint                    | `bigint`                            | `int8`                                     | 8‑byte signed integer                       | `9223372036854775807`                     |
|                | decimal / numeric         | `decimal(p,s)` / `numeric(p,s)`     | —                                         | Exact numeric with precision/scale         | `numeric(10,2)`                           |
|                | real                      | `real`                              | `float4`                                   | 4‑byte single‑precision float              | `3.14::real`                              |
|                | double precision          | `double precision`                 | `float8`                                   | 8‑byte double‑precision float               | `2.718281828459045`                       |
|                | smallserial               | `smallserial`                      | `serial2`                                  | 2‑byte auto‑incrementing integer           | `smallserial`                             |
|                | serial                    | `serial`                            | `serial4`                                  | 4‑byte auto‑incrementing integer           | `serial` PK                               |
|                | bigserial                 | `bigserial`                         | `serial8`                                  | 8‑byte auto‑incrementing integer           | `bigserial`                               |
| **Monetary**    | money                     | `money`                             | —                                         | Fixed‑point currency value                 | `'$1234.56'::money`                       |
| **Character**   | character(n)              | `character(n)`                      | `char(n)`                                  | Fixed‑length blank‑padded string           | `char(5) 'foo  '`                         |
|                | character varying(n)      | `character varying(n)`              | `varchar(n)`                               | Variable‑length string with limit          | `varchar(255)`                            |
|                | text                      | `text`                              | —                                         | Unlimited string                           | `'hello world'::text`                     |
| **Binary**      | bytea                     | `bytea`                             | —                                         | Binary data (“byte array”)                | `'\xDEADBEEF'::bytea`                     |
| **Date/Time**   | date                      | `date`                              | —                                         | Calendar date                              | `DATE '2025-06-12'`                       |
|                | time [without tz]         | `time [ (p) ]`                      | —                                         | Time of day (no timezone)                 | `TIME '13:45:00'`                         |
|                | time with time zone       | `time (p) with time zone`           | `timetz`                                   | Time + timezone                            | `TIME '13:45:00+02'`                      |
|                | timestamp [without tz]    | `timestamp [ (p) ]`                 | —                                         | Date + time (no timezone)                 | `TIMESTAMP '2025-06-12 13:45:00'`         |
|                | timestamp with time zone  | `timestamp (p) with time zone`      | `timestamptz`                              | Date + time + timezone                     | `TIMESTAMPTZ '2025-06-12 13:45:00+02'`    |
|                | interval                  | `interval`                          | —                                         | Time span                                  | `'1 day 02:30'::interval`                 |
| **Boolean**     | boolean                   | `boolean`                           | `bool`                                     | TRUE/FALSE/NULL                             | `TRUE`, `FALSE`                           |
| **Enumerated**  | enum                      | *Custom Type*                       | —                                         | User‑defined ordered labels                | `CREATE TYPE mood AS ENUM ('sad','happy')` |
| **Geometric**   | point                     | `point`                             | —                                         | 2D point (x,y)                             | `'(1,2)'::point`                          |
|                | line                      | `line`                              | —                                         | Infinite line                              | `'(0,0),(1,1)'::line`                     |
|                | lseg                      | `lseg`                              | —                                         | Line segment                               | `'[(0,0),(1,1)]'::lseg`                   |
|                | box                       | `box`                               | —                                         | Rectangular box                            | `'( (0,0),(1,1) )'::box`                  |
|                | path                      | `path`                              | —                                         | Open or closed path                        | `'( (0,0),(1,1),(1,0) )'::path`           |
|                | polygon                   | `polygon`                           | —                                         | Closed polygon                             | `'( (0,0),(1,0),(1,1),(0,1) )'::polygon` |
|                | circle                    | `circle`                            | —                                         | Center + radius                            | `'<(0,0),1>'::circle`                     |
| **Network**     | cidr                      | `cidr`                              | —                                         | IPv4/IPv6 network                          | `'192.168.1.0/24'::cidr`                  |
|                | inet                      | `inet`                              | —                                         | IPv4/IPv6 address                          | `'192.168.1.5'::inet`                     |
|                | macaddr                   | `macaddr`                           | —                                         | MAC address                                | `'08:00:2b:01:02:03'::macaddr`            |
|                | macaddr8                  | `macaddr8`                          | —                                         | 8‑byte MAC address                         | `'08:00:2b:01:02:03:04:05'::macaddr8`     |
| **Bit String**  | bit(n)                    | `bit(n)`                            | —                                         | Fixed‑length bit string                    | `B'1010'::bit(4)`                         |
|                | varbit                    | `bit varying(n)`                    | —                                         | Variable‑length bit string                 | `B'101010'::varbit`                       |
| **Text Search** | tsvector                  | `tsvector`                          | —                                         | Lexeme array for full-text search         | `to_tsvector('english','text')`          |
|                | tsquery                   | `tsquery`                           | —                                         | Text search query                          | `'cat & dog'::tsquery`                   |
| **UUID**        | uuid                      | `uuid`                              | —                                         | Universally Unique Identifier             | `'550e8400-e29b-41d4-a716-446655440000'` |
| **XML**         | xml                       | `xml`                               | —                                         | XML document                               | `'<tag>value</tag>'::xml`                |
| **JSON**        | json                      | `json`                              | —                                         | Textual JSON                               | `'{"a":1}'::json`                         |
|                | jsonb                     | `jsonb`                             | —                                         | Binary JSON (indexed)                      | `'{"a":1}'::jsonb`                        |
| **Arrays**      | anytype[]                 | `<type>[]`                          | —                                         | Array of any type                          | `integer[]`, `text[]`                    |
| **Ranges**      | int4range                 | `int4range`                         | —                                         | Range on ints                               | `int4range(1,10)`                        |
|                | int8range                 | `int8range`                         | —                                         | Range on bigints                           | `int8range(1,10000000000)`              |
|                | numrange                  | `numrange`                          | —                                         | Range on numerics                          | `numrange(1.0,2.0)`                      |
|                | tsrange                   | `tsrange`                           | —                                         | Range on timestamp                         | `tsrange('2025-01-01','2025-12-31')`     |
|                | tstzrange                 | `tstzrange`                         | —                                         | Range on timestamptz                       | `tstzrange('2025-01-01','2025-12-31')`   |
|                | daterange                 | `daterange`                         | —                                         | Range on dates                             | `daterange('2025-01-01','2025-12-31')`   |
| **Composite**   | composite type            | *Custom Type*                       | —                                         | Row type via `CREATE TYPE ... AS (...)`   | `CREATE TYPE foo AS (a int, b text);`    |
| **Domain**      | domain                    | *Custom Type*                       | —                                         | Constraint‑wrapped type                    | `CREATE DOMAIN positive_int AS integer CHECK (VALUE>0);` |
| **Pseudo**      | anyelement, anyarray, ... | *Pseudo‑types*                      | —                                         | Function parameter/result types (not columns) | Used in stored procedures             |

---

## Recon

Show version

```psql
SHOW SERVER_VERSION;
```

Show system status

```sql
\conninfo
```

Show environmental variables

```sql
SHOW ALL;
```

List users

```sql
SELECT rolname FROM pg_roles;
```

Show current user

```sql
SELECT current_user;
```

Show current user's permissions

```sql
\du
```

List databases

```sql
\l
```

Show current database

```sql
SELECT current_database();
```

Show all tables in database

```sql
\dt
```

List functions

```sql
\df <schema>
```

## Databases

List databasees

```sql
\l
```

Connect to database

```sql
\c <database_name>
```

S current database

```sql
SELECT current_database();
```

Create database

<http://www.postgresql.org/docs/current/static/sql-createdatabase.html>

```sql
CREATE DATABASE <database_name> WITH OWNER <username>;
```

##### delete database

<http://www.postgresql.org/docs/current/static/sql-dropdatabase.html>

```sql
DROP DATABASE IF EXISTS <database_name>;
```

##### rename database

<http://www.postgresql.org/docs/current/static/sql-alterdatabase.html>

```sql
ALTER DATABASE <old_name> RENAME TO <new_name>;
```

## Users

List roles

```sql
SELECT rolname FROM pg_roles;
```

Create user

<http://www.postgresql.org/docs/current/static/sql-createuser.html>

```sql
CREATE USER <user_name> WITH PASSWORD '<password>';
```

##### drop user

<http://www.postgresql.org/docs/current/static/sql-dropuser.html>

```sql
DROP USER IF EXISTS <user_name>;
```

##### alter user password

<http://www.postgresql.org/docs/current/static/sql-alterrole.html>

```sql
ALTER ROLE <user_name> WITH PASSWORD '<password>';
```

## Permissions

##### become the postgres user, if you have permission errors

```shell
sudo su - postgres
psql
```

##### grant all permissions on database

<http://www.postgresql.org/docs/current/static/sql-grant.html>

```sql
GRANT ALL PRIVILEGES ON DATABASE <db_name> TO <user_name>;
```

##### grant connection permissions on database

```sql
GRANT CONNECT ON DATABASE <db_name> TO <user_name>;
```

##### grant permissions on schema

```sql
GRANT USAGE ON SCHEMA public TO <user_name>;
```

##### grant permissions to functions

```sql
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO <user_name>;
```

##### grant permissions to select, update, insert, delete, on a all tables

```sql
GRANT SELECT, UPDATE, INSERT ON ALL TABLES IN SCHEMA public TO <user_name>;
```

##### grant permissions, on a table

```sql
GRANT SELECT, UPDATE, INSERT ON <table_name> TO <user_name>;
```

##### grant permissions, to select, on a table

```sql
GRANT SELECT ON ALL TABLES IN SCHEMA public TO <user_name>;
```

## Schema

List schemas

```sql
\dn

SELECT schema_name FROM information_schema.schemata;

SELECT nspname FROM pg_catalog.pg_namespace;
```

Create schema

<http://www.postgresql.org/docs/current/static/sql-createschema.html>

```sql
CREATE SCHEMA IF NOT EXISTS <schema_name>;
```

##### drop schema

<http://www.postgresql.org/docs/current/static/sql-dropschema.html>

```sql
DROP SCHEMA IF EXISTS <schema_name> CASCADE;
```

## Tables

List tables, in current db

```sql
\dt

SELECT table_schema,table_name FROM information_schema.tables ORDER BY table_schema,table_name;
```

List tables, globally

```sql
\dt *.*.

SELECT * FROM pg_catalog.pg_tables
```

List table schema

```sql
\d <table_name>
\d+ <table_name>

SELECT column_name, data_type, character_maximum_length
FROM INFORMATION_SCHEMA.COLUMNS
WHERE table_name = '<table_name>';
```

Create table

<http://www.postgresql.org/docs/current/static/sql-createtable.html>

```sql
CREATE TABLE <table_name>(
  <column_name> <column_type>,
  <column_name> <column_type>
);
```

Create table, with an auto-incrementing primary key

```sql
CREATE TABLE <table_name> (
  <column_name> SERIAL PRIMARY KEY
);
```

##### delete table

<http://www.postgresql.org/docs/current/static/sql-droptable.html>

```sql
DROP TABLE IF EXISTS <table_name> CASCADE;
```

## Columns

##### add column

<http://www.postgresql.org/docs/current/static/sql-altertable.html>

```sql
ALTER TABLE <table_name> IF EXISTS
ADD <column_name> <data_type> [<constraints>];
```

##### update column

```sql
ALTER TABLE <table_name> IF EXISTS
ALTER <column_name> TYPE <data_type> [<constraints>];
```

##### delete column

```sql
ALTER TABLE <table_name> IF EXISTS
DROP <column_name>;
```

##### update column to be an auto-incrementing primary key

```sql
ALTER TABLE <table_name>
ADD COLUMN <column_name> SERIAL PRIMARY KEY;
```

##### insert into a table, with an auto-incrementing primary key

```sql
INSERT INTO <table_name>
VALUES (DEFAULT, <value1>);


INSERT INTO <table_name> (<column1_name>,<column2_name>)
VALUES ( <value1>,<value2> );
```

## Data

##### read all data

<http://www.postgresql.org/docs/current/static/sql-select.html>

```sql
SELECT * FROM <table_name>;
```

##### read one row of data

```sql
SELECT * FROM <table_name> LIMIT 1;
```

# Search for data

```sql
SELECT * FROM <table_name> WHERE <column_name> = <value>;
```

##### insert data

<http://www.postgresql.org/docs/current/static/sql-insert.html>

```sql
INSERT INTO <table_name> VALUES( <value_1>, <value_2> );
```

##### edit data

<http://www.postgresql.org/docs/current/static/sql-update.html>

```sql
UPDATE <table_name>
SET <column_1> = <value_1>, <column_2> = <value_2>
WHERE <column_1> = <value>;
```

##### delete all data

<http://www.postgresql.org/docs/current/static/sql-delete.html>

```sql
DELETE FROM <table_name>;
```

##### delete specific data

```sql
DELETE FROM <table_name>
WHERE <column_name> = <value>;
```

## Scripting

##### run local script, on remote host

<http://www.postgresql.org/docs/current/static/app-psql.html>

```shell
psql -U <username> -d <database> -h <host> -f <local_file>

psql --username=<username> --dbname=<database> --host=<host> --file=<local_file>
```

##### backup database data, everything

<http://www.postgresql.org/docs/current/static/app-pgdump.html>

```shell
pg_dump <database_name>

pg_dump <database_name>
```

##### backup database, only data

```shell
pg_dump -a <database_name>

pg_dump --data-only <database_name>
```

##### backup database, only schema

```shell
pg_dump -s <database_name>

pg_dump --schema-only <database_name>
```

##### restore database data

<http://www.postgresql.org/docs/current/static/app-pgrestore.html>

```shell
pg_restore -d <database_name> -a <file_pathway>

pg_restore --dbname=<database_name> --data-only <file_pathway>
```

##### restore database schema

```shell
pg_restore -d <database_name> -s <file_pathway>

pg_restore --dbname=<database_name> --schema-only <file_pathway>
```

##### export table into CSV file

<http://www.postgresql.org/docs/current/static/sql-copy.html>

```sql
\copy <table_name> TO '<file_path>' CSV
```

##### export table, only specific columns, to CSV file

```sql
\copy <table_name>(<column_1>,<column_1>,<column_1>) TO '<file_path>' CSV
```

##### import CSV file into table

<http://www.postgresql.org/docs/current/static/sql-copy.html>

```sql
\copy <table_name> FROM '<file_path>' CSV
```

##### import CSV file into table, only specific columns

```sql
\copy <table_name>(<column_1>,<column_1>,<column_1>) FROM '<file_path>' CSV
```

## Debugging

<http://www.postgresql.org/docs/current/static/using-explain.html>

<http://www.postgresql.org/docs/current/static/runtime-config-logging.html>

## Advanced Features

<http://www.tutorialspoint.com/postgresql/postgresql_constraints.htm>
