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

## Learn PostgreSQL

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

Good practice: SQL keywords: UPPER CASE

When creating identifiers (names of databases, tables, columns, etc) use `underscore_name`.

**Postgresql treats identifiers case insensitively when not quoted (it actually folds them to lowercase internally), and case sensitively when quoted; many people are not aware of this idiosyncrasy. **

Use plural name like `users`, `audits`. That will avoid collision with reserve words.

*PostGIS* use `geom` as geometry column name to avoid  confusion whith the data type `geometry.`

Use spell out id fields for ID column like `user_id`, `contact_id`.

Avoid ambiguity for name table and columns like  `temperature` vs `temperature_celsius`.

When possible, name foreign key columns the same as the columns they refer to.

Commun words used to name DB columns `created_at`, `updated_at`, `source_id`, `destination_id`.

### Queries

```sql
SELECT columns_name FROM table_names;
```
