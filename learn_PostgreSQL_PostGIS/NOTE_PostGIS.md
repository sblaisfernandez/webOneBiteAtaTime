
# PostGIS

## PostGIS Spatial data Types

- [PostgreSQL Not for professional](https://drive.google.com/drive/u/0/folders/1gnZVVymztzGffrfJttUm5e_7RMx4d9Y-)

- [PostGIS in action](https://drive.google.com/drive/u/0/home)

- Geometry: The planar type.

- Geography: The spheroidal geodetic type.

- Raster: The multiband cell type.

- Topology: The relational

## Spatial Data Types

| Category              | Name                         | SQL Symbol                            | Aliases                                                       | Description                                                                                   | Example                                                                                                       |
|-----------------------|------------------------------|----------------------------------------|----------------------------------------------------------------|-----------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------|
| **Core Geometry**      | Point                        | `geometry(Point, SRID)`                | —                                                              | Single coordinate (2D, 3D, or 4D)                                                            | `ST_GeomFromText('POINT(1 2)', 4326)`                                                                          |
|                       | LineString                   | `geometry(LineString, SRID)`           | —                                                              | Sequence of points forming a line                                                           | `ST_GeomFromText('LINESTRING(0 0,1 1)', 4326)`                                                                 |
|                       | Polygon                      | `geometry(Polygon, SRID)`              | —                                                              | Closed shape with outer ring and possible holes                                             | `ST_GeomFromText('POLYGON((0 0,1 0,1 1,0 0))', 4326)`                                                          |
|                       | MultiPoint                   | `geometry(MultiPoint, SRID)`           | —                                                              | Collection of points                                                                      | `geometry(Point,4326)[]`                                                                                       |
|                       | MultiLineString              | `geometry(MultiLineString, SRID)`      | —                                                              | Collection of lines                                                                         | —                                                                                                              |
|                       | MultiPolygon                 | `geometry(MultiPolygon, SRID)`         | —                                                              | Collection of polygons                                                                      | —                                                                                                              |
|                       | GeometryCollection           | `geometry(GeometryCollection, SRID)`   | —                                                              | Mixed geometry collection                                                                   | —                                                                                                              |
|                       | PolyhedralSurface            | `geometry(PolyhedralSurface, SRID)`    | —                                                              | 3D polygonal surfaces                                                                       | —                                                                                                              |
|                       | Triangle                     | `geometry(Triangle, SRID)`             | —                                                              | 3-point polygon triangle                                                                    | —                                                                                                              |
|                       | TIN                          | `geometry(TIN, SRID)`                  | —                                                              | Triangulated Irregular Network                                                              | —                                                                                                              |
| **Measured/3D variants**| Z (3D)                      | `geometry(PointZ,SRID)` etc.           | `Z` suffix e.g. PointZ, PolygonZ                               | Include elevation                                                                            | `geometry(PointZ,4326)`                                                                                       |
|                       | M (measure)                  | `geometry(PointM,SRID)`                | `M` suffix e.g. MultiLineStringM                              | Include custom measure value                                                                 | —                                                                                                              |
|                       | ZM (3D + measure)           | `geometry(PointZM,SRID)`               | `ZM` suffix                                                    | Both 3D and measure                                                                            | —                                                                                                              |
| **Generic Geometry**   | Geometry                     | `geometry` or `geometry(Geometry,SRID)`| —                                                              | Any geometry subtype                                                                         | `geometry`                                                                                                     |
| **Geography**          | Geography                    | `geography(...)`                      | —                                                              | Spheroidal geospatial data (true ellipsoidal math)                                          | `geography(Point,4326)`                                                                                        |
| **Raster**             | Raster                       | `raster`                               | —                                                              | Gridded data—images, DSMs, remote sensing—multi-band                                         | `raster`                                                                                                       |
| **Topology**           | TopoGeometry                 | `topogeometry`                         | —                                                              | Topological primitives (nodes, edges, faces)—requires `postgis_topology`                     | `topogeometry`                                                                                                 |
| **Bounding Boxes**     | box2d                        | —                                      | `Box2D`                                                        | 2D bounding box type returned by some functions                                              | `ST_Extent(geom)`                                                                                              |
|                       | box3d                        | —                                      | `Box3D`                                                        | 3D bounding box “                                                                | `ST_3DExtent(geom)`                                                                                            |

### Spatial Reference System

A Spatial Reference System defines how the position of points on the Earth's surface is represented in space — through coordinates that are tied to a specific mathematical model of the Earth.

👉 It consists of:

a Datum → defines the size and shape of the Earth (ellipsoid) and how that ellipsoid is aligned to the real Earth (geoid);

a Coordinate system → defines how coordinates (latitude, longitude, height, X/Y/Z, or projected coordinates) are expressed;

a Map projection (optional) → defines how to flatten the Earth's curved surface into a 2D map.

### Spatial Indexing

Spatial Indexing is a method of organizing spatial data (points, lines, polygons) so that spatial queries can be performed very quickly.

👉 Without an index, spatial queries (like ST_Intersects, ST_Within, ST_DWithin, ST_Contains, ST_Distance) would require a full table scan → comparing every geometry → very slow.

👉 With a spatial index, the database can rapidly filter out most geometries and only test the ones that could actually match.

| Index Type                                  | Description                                                                                         |
| ------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| **R-tree / GIST (Generalized Search Tree)** | Most common in PostGIS — stores geometries in a **hierarchical bounding box tree**.                 |
| **Quad-tree**                               | Divides space into 4 quadrants recursively — used in some in-memory engines or vector tile systems. |
| **Grid index**                              | Divides space into fixed grids — sometimes used in combination with others.                         |
