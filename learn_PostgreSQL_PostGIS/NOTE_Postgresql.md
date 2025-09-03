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

## Learn PostgreSQL - Relational Database (RDBMS)

- [Derek Banas Master postgresql](https://www.youtube.com/watch?v=85pG_pDkITY)
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

Avoid ambiguity for name table and columns like `temperatures` vs `temperatures_celsius`.

When possible, name foreign key columns the same as the columns they refer to.

Commun words used to name DB columns `created_at`, `updated_at`, `source_id`, `destination_id`.

### Derek Banas notes Design a Database

- 1 Table represent 1 Real World Object: `Customers`, `Orders`, `Products`, `sales_orders`
- Columns Store 1 Piece of Information: `customers_id`, `name`, `order_id`, `product_id`
- How to table relate to each other: `foreign_key`
- Reduce Redundant Data: Normalization

- [postgresql-tutorial](https://github.com/derekbanas/postgresql-tutorial/tree/main)

## Users

| Task | Command | Type | Notes |
|------|---------|------|-------|
| List roles | `SELECT rolname FROM pg_roles;` | SQL | Equivalent psql meta: `\du` (or `\du+` for attributes). |
| Create user (role with LOGIN) | `CREATE USER <user_name> WITH PASSWORD '<password>';` | SQL | Shorthand for `CREATE ROLE ... LOGIN`. Add options: `VALID UNTIL 'infinity'`, `CREATEDB`, etc. |
| Drop user | `DROP USER IF EXISTS <user_name>;` | SQL | Fails if role owns objects; reassign or drop objects first. |
| Change password | `ALTER ROLE <user_name> WITH PASSWORD '<password>';` | SQL | Use `ALTER ROLE ... PASSWORD NULL` to remove password. |
| Grant all on database | `GRANT ALL PRIVILEGES ON DATABASE <db_name> TO <user_name>;` | SQL | Consider principle of least privilege instead of blanket ALL. |
| Grant connect only | `GRANT CONNECT ON DATABASE <db_name> TO <user_name>;` | SQL | Needed before schema/table grants for fresh roles. |
| Grant usage on schema | `GRANT USAGE ON SCHEMA public TO <user_name>;` | SQL | Required so role can access objects within the schema. |
| Grant table privileges | `GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO <user_name>;` | SQL | For future tables: also run `ALTER DEFAULT PRIVILEGES`. |

## Permissions

Common DML operations:

| Task | Command | Notes |
|------|---------|-------|
| Select all rows | `SELECT * FROM <table_name>;` | Prefer explicit column list in production. |
| Select specific columns | `SELECT <col1>, <col2> FROM <table_name>;` | Replaces erroneous example `columns_name FROM table_names`. |
| Select single row (any) | `SELECT * FROM <table_name> LIMIT 1;` | Add `ORDER BY` for deterministic result. |
| Filter rows | `SELECT * FROM <table_name> WHERE <column_name> = <value>;` | Use parameterized queries to avoid injection. |
| Insert row (positional) | `INSERT INTO <table_name> VALUES (<value_1>, <value_2>);` | Order must match table definition; brittle if schema changes. |
| Insert row (explicit) | `INSERT INTO <table_name> (<column_1>, <column_2>) VALUES (<value_1>, <value_2>);` | Safer—only specified columns. |
| Update rows | `UPDATE <table_name> SET <column_1> = <value_1>, <column_2> = <value_2> WHERE <column_1> = <value>;` | Always include WHERE to avoid full-table updates. |
| Delete all rows | `DELETE FROM <table_name>;` | Consider `TRUNCATE <table_name>;` for faster bulk removal (resets identity). |
| Delete filtered rows | `DELETE FROM <table_name> WHERE <column_name> = <value>;` | Check affected row count. |
| Upsert (optional) | `INSERT INTO <table>(id,col) VALUES($1,$2) ON CONFLICT (id) DO UPDATE SET col=EXCLUDED.col;` | Pattern for merge; requires unique constraint. |
| Insert returning | `INSERT INTO <table_name> (<column_1>) VALUES (<value_1>) RETURNING *;` | RETURNING can list specific columns. |

Common table & column operations:

| Task | Command | Notes |
|------|---------|-------|
| List tables (current search_path) | `\dt` | Uses current `search_path`; add schema pattern: `\dt public.*`. |
| List tables (all schemas) | `\dt *.*` | May include system schemas; filter as needed. |
| List tables via information_schema | `SELECT table_schema, table_name FROM information_schema.tables ORDER BY table_schema, table_name;` | ANSI view; excludes some system catalogs. |
| List tables via catalog | `SELECT * FROM pg_catalog.pg_tables;` | Raw catalog view; includes internal details. |
| Describe table (summary) | `\d <table_name>` | Columns, types, modifiers, indexes. |
| Describe table (extended) | `\d+ <table_name>` | Adds storage, description, size. |
| List columns (SQL) | `SELECT column_name, data_type, character_maximum_length FROM information_schema.columns WHERE table_name = '<table_name>';` | Use for scripting / tooling. |
| Create table (basic) | `CREATE TABLE <table_name> ( <col1> <type1>, <col2> <type2> );` | Define constraints (PK, FK, UNIQUE, CHECK) inline or at end. |
| Create table with serial PK | `CREATE TABLE <table_name> ( id SERIAL PRIMARY KEY, ... );` | Prefer identity: `GENERATED BY DEFAULT AS IDENTITY` in modern Postgres. |
| Drop table (if exists) | `DROP TABLE IF EXISTS <table_name> CASCADE;` | CASCADE removes dependent objects; prefer RESTRICT in production. |
| Add column | `ALTER TABLE <table_name> ADD COLUMN <column_name> <data_type> [<constraints>];` | New column defaults NULL unless DEFAULT specified. |
| Alter column type | `ALTER TABLE <table_name> ALTER COLUMN <column_name> TYPE <data_type> USING <expression>;` | `USING` needed for non-trivial casts. |
| Drop column | `ALTER TABLE <table_name> DROP COLUMN <column_name>;` | Irreversible (except from backup). |
| Add serial / identity PK to existing table | `ALTER TABLE <table_name> ADD COLUMN id SERIAL PRIMARY KEY;` | Identity alternative: `ADD COLUMN id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY;`. |
| Insert row (auto id) | `INSERT INTO <table_name> VALUES (DEFAULT, <value1>);` | Position-based; fragile if schema changes—prefer explicit columns. |
| Insert row (explicit cols) | `INSERT INTO <table_name> (<col1>, <col2>) VALUES (<val1>, <val2>);` | Safer; specify only needed columns. |
| Upsert (insert or update) | `INSERT INTO <table>(id, col) VALUES($1,$2) ON CONFLICT (id) DO UPDATE SET col=EXCLUDED.col;` | Requires unique index / constraint on conflict target. |
| Truncate table | `TRUNCATE <table_name> RESTART IDENTITY CASCADE;` | Fast delete; drops & resets sequences; CASCADE affects FK children. |

## Manipulate Data

### insert data

```sql
INSERT INTO <table_name> VALUES( <value_1>, <value_2> );
```

### Read data

```sql
SELECT * FROM <table_name>;
SELECT columns_name FROM table_names;
```

### read one row of data

```sql
SELECT * FROM <table_name> LIMIT 1;
```

### Search for data

```sql
SELECT * FROM <table_name> WHERE <column_name> = <value>;
```

### edit data

```sql
UPDATE <table_name>
SET <column_1> = <value_1>, <column_2> = <value_2>
WHERE <column_1> = <value>;
```

#### delete all data

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

```shell
psql -U <username> -d <database> -h <host> -f <local_file>

psql --username=<username> --dbname=<database> --host=<host> --file=<local_file>
```

##### backup database data, everything

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
