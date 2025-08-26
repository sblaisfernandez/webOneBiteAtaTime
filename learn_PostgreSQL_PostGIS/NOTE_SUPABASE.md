# Installing Supabase

- [Supabase CLI](https://supabase.com/docs/guides/local-development/cli/getting-started?queryGroups=access-method&access-method=postgres&queryGroups=platform&platform=macos)

- [Migration Example](https://supabase.com/docs/guides/deployment/database-migrations)

Validate supabase is installed.

```bash
supabase --version
brew upgrade supabase
```

Start existing local supabase instance.

```bash
supabase login
supabase projects list
supabase projects create
supabase link

cd <project-folder>

supabase init # Will add supabase/config.toml
```

## Migration workflow first call

```bash
# Fresh new database on the remote
# Add postgis extensions on the remote
supabase migration list
supabase migration fetch
# Update with the remote version of the DB
supabase db pull --schema auth,storage

supabase migration new create_*_tables
# Update script create_*_tables
supabase db diff

supabase migration up

supabase db push

supabase migration list ## Sync of the migration locally and remote
```

## Migration workflow second iteration

```bash
# Fresh new database on the remote
# Add postgis extensions on the remote
supabase migration list
supabase migration fetch # Over right local changes

supabase db diff # Diffs schema changes made to the local or remote database.
supabase db pull --schema auth,storage

supabase migration new create_*_tables
# Update migration
supabase migration up # To apply latest added migration file
supabase migration list # To view additional migration to Local

supabase db push

supabase migration list ## Sync of the migration locally and remote
```

## [Seeding](https://supabase.com/docs/guides/local-development/seeding-your-database)

add file `supabase/seed.sql`
