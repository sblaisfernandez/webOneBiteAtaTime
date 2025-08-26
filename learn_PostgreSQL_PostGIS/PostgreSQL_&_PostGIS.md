
# PostgreSQL & PostGIS

Installing Supabase.

- [Supabase CLI](https://supabase.com/docs/guides/local-development/cli/getting-started?queryGroups=access-method&access-method=postgres&queryGroups=platform&platform=macos)

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

cd <folder>

supabase init # Will add supabase folder
supabase link

supabase migration list
supabase migration fetch
supabase db pull

supabase migration new create_building_tables
```

## PostGIS Spatial data Types

- [PostgreSQL Not for professional](https://drive.google.com/drive/u/0/folders/1gnZVVymztzGffrfJttUm5e_7RMx4d9Y-)

- [PostGIS in action](https://drive.google.com/drive/u/0/home)

- Geometry: The planar type.

- Geography: The spheroidal geodetic type.

- Raster: The multiband cell type.

- Topology: The relational
