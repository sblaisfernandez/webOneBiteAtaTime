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
