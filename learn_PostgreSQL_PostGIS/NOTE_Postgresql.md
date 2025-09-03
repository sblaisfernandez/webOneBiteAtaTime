# Postgres Cheat Sheet

This is a collection of the most common commands I run while administering Postgres databases. The variables shown between the open and closed tags, "<" and ">", should be replaced with a name you choose. Postgres has multiple shortcut functions, starting with a forward slash, "\". Any SQL command that is not a shortcut, must end with a semicolon, ";". You can use the keyboard UP and DOWN keys to scroll the history of previous commands you've run.

## Install in Docker for macOS

```bash
docker pull postgres
docker run --platform linux/arm64 postgres
docker run --name mypostgres -p 5433:5433 -e POSTGRES_USER=mypostgres -e POSTGRES_PASSWORD=mypostgres -d postgres

docker run -it --link mypostgres:postgres --rm postgres \
    sh -c 'exec psql -h "$POSTGRES_PORT_5432_TCP_ADDR" -p "$POSTGRES_PORT_5432_TCP_PORT" -U postgres'
```
docker volume create my-postgis-volume
```bash
docker pull mdillon/postgis
docker run --platform linux/arm64 mdillon/postgis
docker run --name mypostgis -p 5432:5432 -e POSTGRES_USER=mypostgis -e POSTGRES_PASSWORD=mypostgis -d mdillon/postgis

docker run -it --link mypostgis:postgres --rm postgres \
    sh -c 'exec psql -h "$POSTGRES_PORT_5432_TCP_ADDR" -p "$POSTGRES_PORT_5432_TCP_PORT" -U mypostgis'
```

### Recon database

Here’s the recon section condensed into a markdown table:

| Task | Command | Type | Notes |
|------|---------|------|-------|
| Show server version | `SHOW SERVER_VERSION;` | SQL | Returns server version setting (similar to `SELECT version();` for full string). |
| Show connection info | `\conninfo` | psql meta | Current host, port, user, db, SSL. |
| Show all config parameters | `SHOW ALL;` | SQL | Full list of GUC settings. Filter with `WHERE name LIKE 'log_%';` if needed. |
| List roles (users) | `SELECT rolname FROM pg_roles;` | SQL | For details: `\du+` in psql. |
| Show current user | `SELECT current_user;` | SQL | Role after any `SET ROLE`. |
| List roles & attributes | `\du` | psql meta | Shows privileges, role flags (superuser, login, etc.). |
| List databases | `\l` | psql meta | Same as `\list`; includes owner, encoding, collation. |
| Show current database | `SELECT current_database();` | SQL | Database name for current session. |
| List tables (search_path schemas) | `\dt` | psql meta | Add schema: `\dt public.*` or all: `\dt *.*`. |
| List functions (schema) | `\df <schema>` | psql meta | Use `\df+` for more details; omit schema to list all in path. |
| Connect to database | `\c <database_name>` | psql meta | Can also specify user: `\c db user`. |
| Create database | `CREATE DATABASE <database_name> WITH OWNER <username>;` | SQL | Add options: `ENCODING 'UTF8' TEMPLATE template0`. |

## Data Types

| Category        | Name                      | SQL Symbol                         | Aliases                                   | Description                                | Example                                  |
|----------------|---------------------------|-------------------------------------|-------------------------------------------|--------------------------------------------|-------------------------------------------|
| **Numeric**     | smallint                  | `smallint`                          | `int2`                                     | 2‑byte signed integer                       | `-32768` to `32768`                    |
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

## Learn PostgreSQL

# Relational Database (RDBMS)

- [Derek Banas Master postgresl](https://www.youtube.com/watch?v=85pG_pDkITY)
- [SQL course](https://www.freecodecamp.org/news/learn-sql-free-relational-database-courses-for-beginners/)
- [Coursera Introduction to relational Databases](https://www.coursera.org/learn/introduction-to-relational-databases#modules)
- [Course](https://www.youtube.com/watch?v=SpfIwlAYaKk)

## PostgreSQL Style Guide

- [postgres-sql-review-guide](https://www.bytebase.com/blog/postgres-sql-review-guide/)

### PostgreSQL reserved words

```sql
SELECT, INSERT, UPDATE, DELETE, FROM, WHERE, AND, OR, JOIN, CREATE, ALTER, DROP, TABLE, COLUMN, CONSTRAINT, PRIMARY, FOREIGN, KEY, NULL, TRUE, FALSE, CASE, WHEN, THEN, ELSE, END, AS, DISTINCT, GROUP, ORDER, BY, HAVING, IN, EXISTS, UNION, ALL, ANY, SOME, BETWEEN, LIKE, IS, NOT, LIMIT, OFFSET, CAST, COALESCE, EXTRACT.

ABORT, ANALYZE, BINARY, CLUSTER, COPY, DO, EXPLAIN, LISTEN, LOAD, LOCK, MOVE, NOTIFY, RESET, SETOF, SHOW, UNLISTEN, UNTIL, VACUUM, VERBOSE.
```

### Naming tables and columns best practices

Use only english, don't use special characters like ä,é, etc.

Only use lowercase for naming, because SQL is case-insensitive.

*Good practice*: SQL keywords: UPPER CASE

When creating identifiers (names of databases, tables, columns, etc) use `underscore_name`.

**PostgresSQL treats identifiers case insensitively when not quoted (it actually folds them to lowercase internally), and case sensitively when quoted; many people are not aware of this idiosyncrasy.**

Use plural name like `users`, `audits` for table name, that will avoid collision with reserve words.

*PostGIS* use `geom` as geometry column name to avoid confusion with the data type `geometry.`

Use spell out id fields for ID column like `user_id`, `contact_id`.

Avoid ambiguity for name table and columns like `temperature` vs `temperature_celsius`.

When possible, name foreign key columns the same as the columns they refer to.

Commun words used to name DB columns `created_at`, `updated_at`, `source_id`, `destination_id`.

### Derek Banas notes Design a Database

- 1 Table represent 1 Real World Object: `Customers`, `Orders`, `Products`, `sales_orders`
- Columns Store 1 Piece of Information: `customers_id`, `name`, `order_id`, `product_id`
- How to table relate to each other: `foreign_key`
- Reduce Redundant Data: Normalization

```sql
CREATE TYPE sex_type AS enum ('M', 'F')

create table customers (
    first_name text NOT null,
    last_name text NOT NULL,
    email text not null,
    company text,
    street text not null,
    city text not null,
    state text not null,
    zip smallint not null,
    phone varchar(20) not null,
    birth_date Date null,
    sex sex_type not null,
    created_at date not null,
    id serial primary key
)

create table product(
  type_id int references,
  product_type(id),
  name varchar(30) not null,
  supplier varchar(30) not null,
  description text not null,
  id serial primary key);

create table product_type(
  name varchar(30) not null,
  id serial primary key
);

create table item(
  product_id integer references product(id),
  size integer not null,
  color varchar(30) not null,
  picture varchar(30) not null,
  price numeric(6,2) not null,
  id serial primary key
)
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

##### become the postgreSQL user, if you have permission errors

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
SELECT columns_name FROM table_names;
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
