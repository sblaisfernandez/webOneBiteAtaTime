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

## Schemas

```sql
SELECT current_schema();

SELECT schema_name FROM information_schema.schemata ORDER BY schema_name;
```

A PostgreSQL database cluster contains one or more named databases. Roles and a few other object types are shared across the entire cluster. A client connection to the server can only access data in a single database, the one specified in the connection request.

A database contains one or more named schemas, which in turn contain tables. Schemas also contain other kinds of named objects, including data types, functions, and operators. Within one schema, two objects of the same type cannot have the same name.

Furthermore, tables, sequences, indexes, views, materialized views, and foreign tables share the same namespace, so that, for example, an index and a table must have different names if they are in the same schema.

There are several reasons why one might want to use schemas:

- To allow many users to use one database without interfering with each other.

- To organize database objects into logical groups to make them more manageable.

- Third-party applications can be put into separate schemas so they do not collide with the names of other objects.

PostgreSQL automatically creates a schema called public for every new database. Whatever object you create without specifying the schema name, PostgreSQL will place it into this public schema.

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

Each row represents one role and includes details like:

Role name
Whether it can log in
Whether it can create databases
Whether it can create new roles
Whether it’s a superuser
Whether it inherits privileges from roles it’s a member of

```sql
-- List all roles with key attributes
SELECT rolname,
       rolsuper,
       rolcreatedb,
       rolcreaterole,
       rolreplication,
       rolcanlogin,
       rolconnlimit,
       rolvaliduntil
FROM pg_roles;

CREATE USER custom_user WITH PASSWORD 'password';

alter role custom_user with password 'newpassword';

drop  user  if exists custom_user;

-- Select add db
SELECT * FROM pg_database ORDER BY datname;
```

## Privileges

When an object is created, it is assigned an owner. The owner is normally the role that executed the creation statement. For most kinds of objects, the initial state is that only the owner (or a superuser) can do anything with the object. To allow other roles to use it, privileges must be granted.

There are different kinds of privileges: SELECT, INSERT, UPDATE, DELETE, TRUNCATE, REFERENCES, TRIGGER, CREATE, CONNECT, TEMPORARY, EXECUTE, USAGE, SET, ALTER SYSTEM, and MAINTAIN. The privileges applicable to a particular object vary depending on the object's type (table, function, etc.). More detail about the meanings of these privileges appears below. The following sections and chapters will also show you how these privileges are used.

The right to modify or destroy an object is inherent in being the object's owner, and cannot be granted or revoked in itself. (However, like all privileges, that right can be inherited by members of the owning role.

Privilege and role operations:

| Task | Command | Scope | Notes |
|------|---------|-------|-------|
| Become postgres OS user (interactive) | `sudo su - postgres && psql` | OS / session | Needed to issue superuser-level grants when your current role lacks rights. |
| Grant ALL privileges on database | `GRANT ALL PRIVILEGES ON DATABASE <db_name> TO <user_name>;` | Database | Broad privileges; prefer least privilege principle. |
| Grant CONNECT on database | `GRANT CONNECT ON DATABASE <db_name> TO <user_name>;` | Database | Needed before schema/table access if revoked previously. |
| Grant USAGE on schema | `GRANT USAGE ON SCHEMA public TO <user_name>;` | Schema | Allows name resolution; pair with table/function privileges. |
| Grant EXECUTE on all functions | `GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO <user_name>;` | Schema functions | Re-run or set default privileges after adding new functions. |
| Grant DML on all tables | `GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO <user_name>;` | Tables (existing) | Use `ALTER DEFAULT PRIVILEGES` to cover future tables. |
| Grant DML on specific table | `GRANT SELECT, INSERT, UPDATE, DELETE ON <table_name> TO <user_name>;` | Single table | Add `TRUNCATE`, `REFERENCES` as needed. |
| Grant SELECT on all tables | `GRANT SELECT ON ALL TABLES IN SCHEMA public TO <user_name>;` | Read-only | For reporting roles; also grant sequence USAGE if selecting nextval. |

Tip: Default privileges example: `ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO <user_name>;`.

## Roles creation and privileges management best practice

Define roles that encapsulate set of permissions `app_readonly`, `data_analyst`. then assign those roles to a user, rather then directly granting privileges
to a specific user.

- Use non-login roles for grouping

- Create roles without the LOGIN attribute to serve purely as containers for privileges, then grant there 'group' roles to actual login-enabled users.

- Apply the **principle of least privileges**
- Separate administrative and application users

- Strong password policies
- Use scram-sha-256 for password authentification.

- Secure connection method using SSL/TLS

- Change password periodically.

- Don't use SuperUser for application

- Review privileges granted to roles and users periodically.
- Document roles structure
- Monitor user activity, implement logging auditing.

```sql


```

### Presentation For your Eyes Only: Roles, Privileges  and security in postgresql

- [Roles, Privileges  and security in postgresql](https://youtu.be/mtPM3iZFE04?si=33c_hp_yHynVEcme)

#### Users and Groups

Semantically the same as roles

By convention:

User = LOGIN
Group = NOLOGIN

PostgreSQL 8.2+ CREATE (USER | GROUP) is an alias

```sql
CREATE ROLE user1 WITH LOGIN password 'secretpassword' INHERIT;
```

When a user is set by default.  Unless otherwise set, new roles can INHERIT privileges from other roles and have unlimited connection.

**PUBLIC Role**

- All roles are granted implicit membership to PUBLIC.
- the public road cannot be deleted.
- Granted  CONNECT, USAGE, TEMPORARY, and EXECUTE by default.
- >= PG15: NO CREATE on public SCHEMA BY default FOR THE PUBLIC role.
- **BEST PRACTICES**  Revoke all privileges on the public schema from the PUBLIC role. Revoke all database privileges from the PUBLIC role.

```sql
REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON DATABASE db_name FROM PUBLIC;
```

### Privilege Inheritance

- Role can be granted membership into another role.
- If a role has INHERIT set, they automatically have usage of privileges from member roles.
- The preferred method for managing group privileges.

### Providing Object Access

SET ROLE to ap role before creation with correct default privileges.

## Manipulate Data

Common DML operations:

| Task | Command | Notes |
|------|---------|-------|
| Select all rows | `SELECT * FROM <table_name>;` | Prefer explicit column list in production. |
| Select specific columns | `SELECT <col1>, <col2> FROM <table_name>;` | Avoid `SELECT *` for performance and stability. |
| Select single row (any) | `SELECT * FROM <table_name> LIMIT 1;` | Add `ORDER BY` for deterministic result. |
| Filter rows | `SELECT * FROM <table_name> WHERE <column_name> = <value>;` | Parameterize to prevent SQL injection. |
| Insert row (positional) | `INSERT INTO <table_name> VALUES (<value_1>, <value_2>);` | Column order sensitive; fragile if schema changes. |
| Insert row (explicit) | `INSERT INTO <table_name> (<column_1>, <column_2>) VALUES (<value_1>, <value_2>);` | Safer—only specified columns. |
| Insert returning | `INSERT INTO <table_name> (<column_1>) VALUES (<value_1>) RETURNING *;` | Limit RETURNING list for large tables. |
| Upsert (merge) | `INSERT INTO <table>(id,col) VALUES($1,$2) ON CONFLICT (id) DO UPDATE SET col=EXCLUDED.col;` | Requires PK or unique index on conflict target. |
| Update rows | `UPDATE <table_name> SET <column_1> = <value_1>, <column_2> = <value_2> WHERE <column_1> = <value>;` | Always include WHERE; inspect row count. |
| Delete filtered rows | `DELETE FROM <table_name> WHERE <column_name> = <value>;` | Check `RETURNING` for confirmation. |
| Delete all rows | `DELETE FROM <table_name>;` | Consider `TRUNCATE <table_name>;` for faster bulk purge + identity reset. |
| Truncate table | `TRUNCATE <table_name> RESTART IDENTITY CASCADE;` | Fast, resets sequences; CASCADE affects referencing tables. |

## Scripting

Script and backup / restore operations:

| Task | Command | Notes |
|------|---------|-------|
| Run local SQL file on remote host | `psql -h <host> -U <username> -d <database> -f <local_file>` | Long option form: `psql --host=... --username=... --dbname=... --file=...`. Requires network access & permissions. |
| Full logical backup (schema+data) | `pg_dump <database_name> > dump.sql` | Produces plain SQL; use `-Fc` for custom format enabling parallel restore. |
| Backup data only | `pg_dump -a <database_name> > data.sql` | Long form: `--data-only`; excludes schema definitions. |
| Backup schema only | `pg_dump -s <database_name> > schema.sql` | Long form: `--schema-only`; no table data. |
| Restore (custom format) | `pg_restore -d <database_name> <file_path>` | Use with dumps created via `pg_dump -Fc`; add `-j <n>` for parallel threads. |
| Restore data only (custom) | `pg_restore -d <database_name> -a <file_path>` | Long form: `--data-only`; target DB & objects must already exist (unless using `-c`). |
| Restore schema only (custom) | `pg_restore -d <database_name> -s <file_path>` | Long form: `--schema-only`; creates object definitions only. |
| Export table to CSV (server side) | `\copy <table_name> TO '<file_path>' CSV` | Uses psql's `\copy` (client-side); add `HEADER` for column headers. |
| Export selected columns to CSV | `\copy <table_name>(<col1>,<col2>,<col3>) TO '<file_path>' CSV` | Order dictates column order in file. |
| Import CSV into table | `\copy <table_name> FROM '<file_path>' CSV` | Ensure file encodes text correctly (UTF-8); add `HEADER` if file has header row. |
| Import selected columns from CSV | `\copy <table_name>(<col1>,<col2>,<col3>) FROM '<file_path>' CSV` | Omitted columns use defaults / NULL. |
| Faster bulk load (binary) | `\copy <table_name> FROM '<file_path>' (FORMAT binary)` | Requires matching binary format file (`pg_dump -Fc` isn't directly used here). |
| Terminate conflicting sessions (pre-restore) | `SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname='<database_name>' AND pid <> pg_backend_pid();` | Use cautiously; disconnects users. |
| Parallel dump | `pg_dump -Fd -j 4 -f <dir_path> <database_name>` | Directory format; combine with `pg_restore -d <db> -j 4 <dir_path>`. |
| Compressed dump | `pg_dump -Fc <database_name> > dump.custom` | Custom format; can be selectively restored. |

Reference: [COPY docs](https://www.postgresql.org/docs/current/sql-copy.html)

## Debugging

<http://www.postgresql.org/docs/current/static/using-explain.html>

<http://www.postgresql.org/docs/current/static/runtime-config-logging.html>

## Advanced Features

<http://www.tutorialspoint.com/postgresql/postgresql_constraints.htm>
