# PostGIS

![History spatial SQL](./public/images/history-spatial-sql.png)

- [PostGIS Workshop](https://docs.google.com/presentation/d/1tOrp4MQebozybREHYDlE2ZQRlM9Dkne-nRMyCRWc6KY/edit?slide=id.gd85280829a_0_61#slide=id.gd85280829a_0_61)
- [PostgreSQL Not for professional](https://drive.google.com/drive/u/0/folders/1gnZVVymztzGffrfJttUm5e_7RMx4d9Y-)
- [PostGIS in action](https://drive.google.com/drive/u/0/home)

## 4.1. Spatial Data Model

- Geometry: The planar type.
- Geography: The spheroidal geodetic type.
- Raster: The multiband cell type.
- Topology: The relational

- [Data Management](https://postgis.net/docs/manual-3.6/using_postgis_dbmanagement.html#RefObject)

## Point

Coordinates may contain optional Z and M ordinate values. The Z ordinate is often used to represent elevation. The M ordinate contains a measure value, which may represent time or distance. If Z or M values are present in a geometry value, they must be defined for each point in the geometry. If a geometry has Z or M ordinates the coordinate dimension is 3D; if it has both Z and M the coordinate dimension is 4D.

```sql
POINT (1 2)
POINT Z (1 2 3)
POINT ZM (1 2 3 4)
```

## 4.2. Geometry Data Type

The basis for the PostGIS geometry data type is a plane. The shortest path between two points on the plane is a straight line. That means functions on geometries (areas, distances, lengths, intersections, etc) are calculated using straight line vectors and cartesian mathematics. This makes them simpler to implement and faster to execute.

## 4.3 Geography Data Type

The PostGIS geography data type provides native support for spatial features represented on "geographic" coordinates (sometimes called "geodetic" coordinates, or "lat/lon", or "lon/lat"). Geographic coordinates are spherical coordinates expressed in angular units (degrees).

The spatial type modifier restricts the kind of shapes and dimensions allowed in the column. Values allowed for the spatial type are: POINT, LINESTRING, POLYGON, MULTIPOINT, MULTILINESTRING, MULTIPOLYGON, GEOMETRYCOLLECTION. The geography type does not support curves, TINS, or POLYHEDRALSURFACEs.

## 4.4 Geometry Validation

![Geometry Type Tree](./public/images/geometry-tree.png)

| Category        | Name           | SQL Symbol| Aliases             | Description             | Example     |
|-----------------|------------------------------|-|-|-|-|
| **OGC Geometry**| Point| `geometry(Point, SRID)`  | —| Single coordinate (2D, 3D, or 4D)| `ST_GeomFromText('POINT(1 2)', 4326`|
|                 | LineString| `geometry(LineString, SRID)` | —  | Sequence of points forming a line | `ST_GeomFromText('LINESTRING(0 0,1 1)', 4326)`|
|                 | LinearRing| `geometry(LINEARRING, SRID)` | —  | Sequence of points forming a line | `ST_GeomFromText('LINEARRING(0 0,1 1)', 4326)`|
|                 | Polygon   | `geometry(Polygon, SRID)`| —  | Closed shape with outer ring and possible holes | `ST_GeomFromText('POLYGON((0 0,1 0,1 1,0 0))', 4326)`|
|                 | MultiPoint| `geometry(MultiPoint, SRID)`| —  | Collection of points | `geometry(Point,4326)[]`|
|                 | MultiLineString| `geometry(MultiLineString, SRID)`| —  | Collection of lines| —|
|                 | MultiPolygon   | `geometry(MultiPolygon, SRID)`   | —  | Collection of polygons | —|
|                 | GeometryCollection| `geometry(GeometryCollection, SRID)`   | —  | Mixed geometry collection  | —|
|                 | PolyhedralSurface| `geometry(PolyhedralSurface, SRID)`| —  | 3D polygonal surfaces  | —|
|                 | Triangle  | `geometry(Triangle, SRID)` | —  | 3-point polygon triangle   | —    |
|                 | TIN   | `geometry(TIN, SRID)`    | —  | Triangulated Irregular Network  | —   |
| **Measured/3D variants**| Z (3D)   | `geometry(PointZ,SRID)` etc.| `Z` suffix e.g. PointZ, PolygonZ| Include elevation| `geometry(PointZ,4326)`|
|                 | M (measure)    | `geometry(PointM,SRID)`  | `M` suffix e.g. MultiLineStringM | Include custom measure value| —    |
|                 | ZM (3D + measure)| `geometry(PointZM,SRID)` | `ZM` suffix| Both 3D and measure | —    |
| **Generic Geometry**   | Geometry  | `geometry` or `geometry(Geometry,SRID)`| —  | Any geometry subtype    | `geometry`   |
| **Geography**    | Geography | `geography(...)`   | —    | Spheroidal geospatial data (true ellipsoidal math)| `geography(Point,4326)`|
| **Raster** | Raster| `raster`  | —    | Gridded data—images, DSMs, remote sensing—multi-band      | `raster`|
| **Topology**           | TopoGeometry     | `topogeometry`  | —    | Topological primitives (nodes, edges, faces)—requires `postgis_topology`  | `topogeometry`     |
| **Bounding Boxes**     | box2d | —   | `Box2D`          | 2D bounding box type returned by some functions| `ST_Extent(geom)`  |
|                   | box3d | —   | `Box3D`          | 3D bounding box “        | `ST_3DExtent(geom)`|
| **SQL/MM Curves** | CircularString | `geometry(CircularString, SRID)` | —       | Curved line made of one or more circular arcs; each arc is defined by three points (start, control, end). Must have an odd number of points > 1. A closed circle repeats the start/end and uses the middle point opposite on the diameter.  | `ST_GeomFromText('CIRCULARSTRING(0 0,1 1,1 0)', 4326)`                                                                                                                   |
|                   | CompoundCurve  | `geometry(CompoundCurve, SRID)`  | —       | Single continuous curve mixing arc segments and straight LineString segments; each component’s end point must equal the next component’s start point.                                                                                       | `ST_GeomFromText('COMPOUNDCURVE(CIRCULARSTRING(0 0,1 1,1 0),(1 0,0 1))', 4326)`                                                                                          |
|                   | CurvePolygon   | `geometry(CurvePolygon, SRID)`   | —       | Polygon whose rings may be CircularString or CompoundCurve (as well as LineString). PostGIS supports compound curves in curve polygons.                                                                                                     | `ST_GeomFromText('CURVEPOLYGON(CIRCULARSTRING(0 0,4 0,4 4,0 4,0 0),(1 1,3 3,3 1,1 1))', 4326)`                                                                           |
|                   | MultiCurve     | `geometry(MultiCurve, SRID)`     | —       | Collection of curves; members can be LineString, CircularString, or CompoundCurve.                                                                                                                                                          | `ST_GeomFromText('MULTICURVE((0 0,5 5), CIRCULARSTRING(4 0,4 4,8 4))', 4326)`                                                                                            |
|                   | MultiSurface   | `geometry(MultiSurface, SRID)`   | —       | Collection of surfaces; members may be (linear) Polygon or CurvePolygon.                                                                                                                                                                    | `ST_GeomFromText('MULTISURFACE(CURVEPOLYGON(CIRCULARSTRING(0 0,4 0,4 4,0 4,0 0),(1 1,3 3,3 1,1 1)), ((10 10,14 12,11 10,10 10),(11 11,11.5 11,11 11.5,11 11)))', 4326)`  |

### 4.2.1. PostGIS EWKB and EWKT

OGC SFA specifications initially supported only 2D geometries, and the geometry SRID is not included in the input/output representations. The OGC SFA specification 1.2.1 (which aligns with the ISO 19125 standard) adds support for 3D (ZYZ) and measured (XYM and XYZM) coordinates, but still does not include the SRID value.

Because of these limitations PostGIS defined extended EWKB and EWKT formats. They provide 3D (XYZ and XYM) and 4D (XYZM) coordinate support and include SRID information.

### 4.3. Geography Data Type

The PostGIS geography data type provides native support for spatial features represented on "geographic" coordinates (sometimes called "geodetic" coordinates, or "lat/lon", or "lon/lat"). Geographic coordinates are spherical coordinates expressed in angular units (degrees).

The shortest path between two points on the sphere is a great circle arc. Functions on geographies (areas, distances, lengths, intersections, etc) are calculated using arcs on the sphere. By taking the spheroidal shape of the world into account, the functions provide more accurate results.

The spatial type modifier restricts the kind of shapes and dimensions allowed in the column. Values allowed for the spatial type are: POINT, LINESTRING, POLYGON, MULTIPOINT, MULTILINESTRING, MULTIPOLYGON, GEOMETRYCOLLECTION. The geography type does not support curves, TINS, or POLYHEDRALSURFACEs.

**Best practices to create a table with a column of data type geography**

It is possible to have more than one geometry column in a table.

```sql
-- 1) Simple "places" table with a geography Point in WGS84
CREATE TABLE public.places (
  place_id    bigserial PRIMARY KEY,
  name        text NOT NULL,
  -- geography enforces type + SRID via typmod
  geog        geography(Point, 4326) NOT NULL
);

-- 2) Spatial index (uses GiST operator class for geography)
CREATE INDEX places_geog_gix
  ON public.places
  USING GIST (geog);

-- 3) (Optional) Generated geography from lon/lat columns
CREATE TABLE public.stations (
  station_id  bigserial PRIMARY KEY,
  lon         double precision NOT NULL CHECK (lon BETWEEN -180 AND 180),
  lat         double precision NOT NULL CHECK (lat BETWEEN  -90 AND  90),
  geog        geography(Point, 4326)
              GENERATED ALWAYS AS (
                ST_SetSRID(ST_MakePoint(lon, lat), 4326)::geography
              ) STORED
);

CREATE INDEX stations_geog_gix
  ON public.stations
  USING GIST (geog);

-- Example insert
INSERT INTO public.places (name, geog)
VALUES ('CN Tower', 'SRID=4326;POINT(-79.3871 43.6426)'::geography);
```

## Spatial Reference Systems identifier (SRID)

```sql
-- Write a query to list all SRID in the table spatial_ref_sys
SELECT DISTINCT srid, auth_name, auth_srid, srtext FROM public.spatial_ref_sys ORDER BY srid;

-- Write a query to count all SRID in the table spatial_ref_sys
SELECT COUNT(DISTINCT srid) AS srid_count FROM public.spatial_ref_sys;

srid_count|
----------+
      8500|
```

A Spatial Reference System defines how the position of points on the Earth's surface is represented in space — through coordinates that are tied to a specific mathematical model of the Earth.

👉  It consists of:

a Datum → defines the size and shape of the Earth (ellipsoid) and how that ellipsoid is aligned to the real Earth (geoid);

a Coordinate system → defines how coordinates (latitude, longitude, height, X/Y/Z, or projected coordinates) are expressed;

a Map projection (optional) → defines how to flatten the Earth's curved surface into a 2D map.

## Spatial Indexes

![Spatial Indexes](./public/images/spatial-indexes.png)

Spatial Indexing is a method of organizing spatial data (points, lines, polygons) so that spatial queries can be performed very quickly.

👉 Without an index, spatial queries (like ST_Intersects, ST_Within, ST_DWithin, ST_Contains, ST_Distance) would require a full table scan → comparing every geometry → very slow.

👉 With a spatial index, the database can rapidly filter out most geometries and only test the ones that could actually match.

| Index Type               | Description             |
| ------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| **R-tree / GIST (Generalized Search Tree)** | Most common in PostGIS — stores geometries in a **hierarchical bounding box tree**.                 |
| **Quad-tree**            | Divides space into 4 quadrants recursively — used in some in-memory engines or vector tile systems. |
| **Grid index**           | Divides space into fixed grids — sometimes used in combination with others.                         |

## Spatial Functions
