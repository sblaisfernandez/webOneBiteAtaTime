# %% [markdown]
# # Spatial Temporal Functions
#
#
# - [PostGIS Special Functions Index](https://postgis.net/docs/manual-3.2/PostGIS_Special_Functions_Index.html)
# - [PostGIS Reference](https://postgis.net/docs/reference.html#PostGIS_Types)

# %% [markdown]
# ## ST_Area(geometry g1) => `float`
#
# - [ST\_Area](http://postgis.net/docs/ST_Area.html): Returns the area of the surface if it is a polygon or
# multi-polygon. For "geometry" type area is in SRID units. For
# "geography" area is in square meters.
#
# ```sql
# select ST_Area(geom) sqft,
#     ST_Area(geom) * 0.3048 ^ 2 sqm
# from (
#          select 'SRID=2249;POLYGON((743238 2967416,743238 2967450,
# 				 743265 2967450,743265.625 2967416,743238 2967416))' :: geometry geom
#      ) subquery;
# ┌─────────┬─────────────┐
# │  sqft   │     sqm     │
# ├─────────┼─────────────┤
# │ 928.625 │ 86.27208552 │
# └─────────┴─────────────┘
# ```

# %% [markdown]
# ## ST_AsBinary(geometry g1) => bytea
#
# - [ST_AsBinary](http://postgis.net/docs/ST_AsBinary.html): Returns the Well-Known Binary (WKB) representation of the geometry/geography without SRID metadata.
#
# ```sql
# SELECT ST_AsBinary(ST_GeomFromText('POINT(1 2)'));
# -- result
# \x0101000000000000000000f03f0000000000000040
# ```
#
# ## ST_AsText(geometry g1) => text
#
# - [ST_AsText](http://postgis.net/docs/ST_AsText.html): Returns the Well-Known Text (WKT) representation of the geometry/geography without SRID metadata.
#
# ```sql
# SELECT ST_AsText(ST_GeomFromText('POINT(1 2)'));
# -- result
# POINT(1 2)
# ```
# ## ST_Contains(geometry A, geometry B) => boolean
#
# - [ST_Contains(geometry A, geometry B)](http://postgis.net/docs/ST_Contains.html): Returns true if and only if no points of B lie in the exterior of A, and at least one point of the interior of B lies in the interior of A.
#
# ```sql
# SELECT ST_Contains('POLYGON((0 0, 4 0, 4 4, 0 4, 0 0))'::geometry, 'POINT(2 2)'::geometry);
#  st_contains
# -------------
# t
# ```
# ## ST_Crosses(geometry A, geometry B) => boolean
#
# - [ST_Crosses(geometry A, geometry B)](http://postgis.net/docs/ST_Crosses.html): Compares two geometry objects and returns true if their intersection "spatially crosses"; that is, the geometries have some, but not all interior points in common.
#
# ```sql
# SELECT ST_Crosses('LINESTRING(0 0, 2 2)'::geometry, 'LINESTRING(0 2, 2 0)'::geometry);
#  st_crosses
# ------------
# t
# ## ST_Equals(geometry g1) => boolean
#
# - [ST_Equals(geometry A, geometry
# B)](http://postgis.net/docs/ST_Equals.html): Returns true if the given
# geometries represent the same geometry. Directionality is ignored.
#
#
# ```sql
# SELECT name, geom, ST_AsText(geom) FROM nyc_subway_stations WHERE name = 'Broad St';
# ```
# ## ST_Disjoint(geometry A, geometry B) => boolean
#
# - [ST_Disjoint(geometry A, geometry B)](http://postgis.net/docs/ST_Disjoint.html): Returns true if two geometries are disjoint. Geometries are disjoint if they have no point in common.
#
# ```sql
# SELECT ST_Disjoint('POINT(0 0)'::geometry, 'LINESTRING ( 1 1, 2 2 )'::geometry);
#  st_disjoint
# -------------
# t
#
# ## ST_Distance(geometry A, geometry B) => float
#
# - [ST_Distance](http://postgis.net/docs/ST_Distance.html): Returns the 2-dimensional cartesian minimum distance (based on spatial reference) between two geometries in projected units.
#
# ```sql
# SELECT ST_Distance('POINT(0 0)'::geometry, 'POINT(3 4)'::geometry);
# -- result
# st_distance
# -------------
# ```
#
# ## ST_DWithin(geometry A, geometry B, double precision distance_of_srid) => boolean
#
# - [ST_DWithin](http://postgis.net/docs/ST_DWithin.html): Returns true if the geometries are within the specified distance of one another. Uses index if available.
#
# ```sql
# SELECT ST_DWithin('POINT(0 0)'::geometry, 'POINT(1 1)'::geometry, 1.5);
# -- result
# t
# ```
#
# ## ST_GeometryType(geometry g1) => `text`
#
# - [ST\_GeometryType](http://postgis.net/docs/ST_GeometryType.html): Returns the geometry type of the ST\_Geometry
# value.
#
# ```sql
# SELECT ST_GeometryType(ST_GeomFromText('LINESTRING(77.29 29.07,77.42 29.26,77.27 29.31,77.29 29.07)'));
# --result
# ST_LineString
# ```
# ## ST_Intersects(geometry A, geometry B) => boolean
#
# - [ST_Intersects(geometry A, geometry B)](http://postgis.net/docs/ST_Intersects.html): Returns TRUE if the
# Geometries/Geography \"spatially intersect\" - (share any portion of space) and FALSE if they don\'t (they are Disjoint).
#
# ```sql
# SELECT ST_Intersects('POINT(0 0)'::geometry, 'LINESTRING ( 0 0, 0 2 )'::geometry);
#  st_intersects
# ---------------
# t
# ```
# ## ST_Overlaps(geometry A, geometry B) => boolean
#
# - [ST_Overlaps(geometry A, geometry B)](http://postgis.net/docs/ST_Overlaps.html): Returns TRUE if the Geometries share space, are of the same dimension, but are not completely contained by each other.
#
# ```sql
# SELECT ST_Overlaps('POLYGON((0 0, 2 0, 2 2, 0 2, 0 0))'::geometry, 'POLYGON((1 1, 3 1, 3 3, 1 3, 1 1))'::geometry);
# st_overlaps
# -------------
# t
# ```
# ## ST_Touches(geometry A, geometry B) => boolean
#
# - [ST_Touches(geometry A, geometry B)](http://postgis.net/docs/ST_Touches.html): Returns TRUE if the geometries have at least one point in common, but their interiors do not intersect.
#
# ```sql
# SELECT ST_Touches('POLYGON((0 0, 2 0, 2 2, 0 2, 0 0))'::geometry, 'LINESTRING(2 0, 2 2)'::geometry);
#  st_touches
# ------------
# t
# ```
# ## ST_Union(geometry g1, geometry g2, float8, gridSize) => geometry
#
# - geometry ST_Union(geometry g1, geometry g2);
# - geometry ST_Union(geometry g1, geometry g2, float8 gridSize);
# - geometry ST_Union(geometry[] g1_array);
# - geometry ST_Union(geometry set g1field);
# - geometry ST_Union(geometry set g1field, float8 gridSize);
#
# Unions the input geometries, merging geometry to produce a result geometry with no overlaps. The output may be an atomic geometry, a MultiGeometry, or a Geometry Collection.
#
# - [ST\_Union](http://postgis.net/docs/ST_Union.html): Returns a geometry representing the point-set union of the input geometries.
#
# ```sql
# select ST_AsText(ST_Union('POINT(1 2)' :: geometry, 'POINT(-2 3)' :: geometry))
#
# st_asText
# ----------
# MULTIPOINT(-2 3,1 2)
# ```
# ## ST_Within(geometry A, geometry B) => boolean
#
# - [ST_Within(geometry A, geometry B)](https://postgis.net/docs/ST_Within.html): Returns true if the geometry A is completely inside geometry B.
#
# ```sql
# SELECT ST_Within('POINT(1 1)'::geometry, 'POLYGON((0 0, 2 0, 2 2, 0 2, 0 0))'::geometry);
#  st_within
# -----------
# t
# ```
# ## ST_X(geometry g1) => float
#
#
# - [ST\_X](http://postgis.net/docs/ST_X.html): Return the X coordinate of the point, or NULL if not available. Input must be a point.
#
# ```sql
# SELECT ST_X(ST_GeomFromEWKT('POINT(1 2 3 4)'));
#  st_x
# ------
# 1
# ```
# ## ST_Y(geometry g1) => float
#
# - [ST_Y](http://postgis.net/docs/ST_Y.html): Returns the Y coordinate of the point, or NULL if not available. Input must be a point.
#
# ```sql
# SELECT ST_Y(ST_GeomFromEWKT('POINT(1 2 3 4)'));
#  st_y
# ------
# 2
# ```
# ## ST_EndPoint(geometry g1) => geometry
#
# - [ST_EndPoint](http://postgis.net/docs/ST_EndPoint.html): Returns the last point of a LINESTRING geometry as a POINT.
#
# ```sql
# SELECT ST_EndPoint('LINESTRING(0 0, 1 1, 2 2)'::geometry);
# -- result
# POINT(2 2)
# ```
#
# ## ST_AsEWKB(geometry g1) => bytea
#
# - [ST_AsEWKB](http://postgis.net/docs/ST_AsEWKB.html): Returns the Well-Known Binary (WKB) representation of the geometry with SRID metadata.
#
# ```sql
# SELECT ST_AsEWKB(ST_GeomFromText('POINT(1 2)', 4326));
# -- result
# \x0101000020e6100000000000000000f03f0000000000000040
# ```
#
# ## ST_AsEWKT(geometry g1) => text
#
# - [ST_AsEWKT](http://postgis.net/docs/ST_AsEWKT.html): Returns the Well-Known Text (WKT) representation of the geometry with SRID metadata.
#
# ```sql
# SELECT ST_AsEWKT(ST_GeomFromText('POINT(1 2)', 4326));
# -- result
# SRID=4326;POINT(1 2)
# ```
#
# ## ST_AsGeoJSON(geometry g1) => text
#
# - [ST_AsGeoJSON](http://postgis.net/docs/ST_AsGeoJSON.html): Returns the geometry as a GeoJSON element.
#
# ```sql
# SELECT ST_AsGeoJSON(ST_GeomFromText('POINT(1 2)', 4326));
# -- result
# {"type":"Point","coordinates":[1,2]}
# ```
#
# ## ST_AsGML(geometry g1) => text
#
# - [ST_AsGML](http://postgis.net/docs/ST_AsGML.html): Returns the geometry as a GML version 2 or 3 element.
#
# ```sql
# SELECT ST_AsGML(ST_GeomFromText('POINT(1 2)', 4326));
# -- result
# <gml:Point srsName="EPSG:4326"><gml:coordinates>1,2</gml:coordinates></gml:Point>
# ```
#
# ## ST_AsKML(geometry g1) => text
#
# - [ST_AsKML](http://postgis.net/docs/ST_AsKML.html): Returns the geometry as a KML element. Several variants. Default version=2, default precision=15.
#
# ```sql
# SELECT ST_AsKML(ST_GeomFromText('POINT(1 2)', 4326));
# -- result
# <Point><coordinates>1,2</coordinates></Point>
# ```
#
# ## ST_AsSVG(geometry g1) => text
#
# - [ST_AsSVG](http://postgis.net/docs/ST_AsSVG.html): Returns a Geometry in SVG path data given a geometry or geography object.
#
# ```sql
# SELECT ST_AsSVG(ST_GeomFromText('POINT(1 2)', 4326));
# -- result
# <circle cx="1" cy="-2" r="1" />
# ```
#
# ## ST_ExteriorRing(geometry g1) => geometry
#
# - [ST_ExteriorRing](http://postgis.net/docs/ST_ExteriorRing.html): Returns a line string representing the exterior ring of the POLYGON geometry. Return NULL if the geometry is not a polygon. Will not work with MULTIPOLYGON.
#
# ```sql
# SELECT ST_ExteriorRing(ST_GeomFromText('POLYGON((0 0, 1 1, 1 0, 0 0))'));
# -- result
# LINESTRING(0 0, 1 1, 1 0, 0 0)
# ```
#
# ## ST_GeometryN(geometry g1, integer n) => geometry
#
# - [ST_GeometryN](http://postgis.net/docs/ST_GeometryN.html): Returns the 1-based Nth geometry if the geometry is a GEOMETRYCOLLECTION, MULTIPOINT, MULTILINESTRING, MULTICURVE or MULTIPOLYGON. Otherwise, return NULL.
#
# ```sql
# SELECT ST_GeometryN('MULTIPOINT((0 0), (1 1), (2 2))'::geometry, 2);
# -- result
# POINT(1 1)
# ```
#
# ## ST_GeomFromGML(text gml) => geometry
#
# - [ST_GeomFromGML](http://postgis.net/docs/ST_GeomFromGML.html): Takes as input GML representation of geometry and outputs a PostGIS geometry object.
#
# ```sql
# SELECT ST_GeomFromGML('<gml:Point srsName="EPSG:4326"><gml:coordinates>1,2</gml:coordinates></gml:Point>');
# -- result
# POINT(1 2)
# ```
#
# ## ST_GeomFromKML(text kml) => geometry
#
# - [ST_GeomFromKML](http://postgis.net/docs/ST_GeomFromKML.html): Takes as input KML representation of geometry and outputs a PostGIS geometry object.
#
# ```sql
# SELECT ST_GeomFromKML('<Point><coordinates>1,2</coordinates></Point>');
# -- result
# POINT(1 2)
# ```
#
# ## ST_GeomFromText(text wkt) => geometry
#
# - [ST_GeomFromText](http://postgis.net/docs/ST_GeomFromText.html): Returns a specified ST_Geometry value from Well-Known Text representation (WKT).
#
# ```sql
# SELECT ST_GeomFromText('POINT(1 2)');
# -- result
# POINT(1 2)
# ```
#
# ## ST_GeomFromWKB(bytea wkb) => geometry
#
# - [ST_GeomFromWKB](http://postgis.net/docs/ST_GeomFromWKB.html): Creates a geometry instance from a Well-Known Binary geometry representation (WKB) and optional SRID.
#
# ```sql
# SELECT ST_GeomFromWKB('\x0101000000000000000000f03f0000000000000040');
# -- result
# POINT(1 2)
# ```
#
# ## ST_InteriorRingN(geometry g1, integer n) => geometry
#
# - [ST_InteriorRingN](http://postgis.net/docs/ST_InteriorRingN.html): Returns the Nth interior linestring ring of the polygon geometry. Return NULL if the geometry is not a polygon or the given N is out of range.
#
# ```sql
# SELECT ST_InteriorRingN('POLYGON((0 0, 4 0, 4 4, 0 4, 0 0), (1 1, 2 1, 2 2, 1 2, 1 1))'::geometry, 1);
# -- result
# LINESTRING(1 1, 2 1, 2 2, 1 2, 1 1)
# ```
#
# ## ST_Length(geometry g1) => float
#
# - [ST_Length](http://postgis.net/docs/ST_Length.html): Returns the 2d length of the geometry if it is a linestring or multilinestring. Geometry are in units of spatial reference.
#
# ```sql
# SELECT ST_Length('LINESTRING(0 0, 3 4)'::geometry);
# -- result
# 5
# ```
#
# ## ST_NDims(geometry g1) => integer
#
# - [ST_NDims](http://postgis.net/docs/ST_NDims.html): Returns coordinate dimension of the geometry as a small int. Values are: 2, 3 or 4.
#
# ```sql
# SELECT ST_NDims('POINT(1 2 3)'::geometry);
# -- result
# 3
# ```
#
# ## ST_NPoints(geometry g1) => integer
#
# - [ST_NPoints](http://postgis.net/docs/ST_NPoints.html): Returns the number of points (vertexes) in a geometry.
#
# ```sql
# SELECT ST_NPoints('LINESTRING(0 0, 1 1, 2 2)'::geometry);
# -- result
# 3
# ```
#
# ## ST_NRings(geometry g1) => integer
#
# - [ST_NRings](http://postgis.net/docs/ST_NRings.html): If the geometry is a polygon or multi-polygon returns the number of rings.
#
# ```sql
# SELECT ST_NRings('POLYGON((0 0, 4 0, 4 4, 0 4, 0 0), (1 1, 2 1, 2 2, 1 2, 1 1))'::geometry);
# -- result
# 2
# ```
#
# ## ST_NumGeometries(geometry g1) => integer
#
# - [ST_NumGeometries](http://postgis.net/docs/ST_NumGeometries.html): If geometry is a GEOMETRYCOLLECTION (or MULTI*) returns the number of geometries, otherwise return NULL.
#
# ```sql
# SELECT ST_NumGeometries('MULTIPOINT((0 0), (1 1), (2 2))'::geometry);
# -- result
# 3
# ```
#
# ## ST_Perimeter(geometry g1) => float
#
# - [ST_Perimeter](http://postgis.net/docs/ST_Perimeter.html): Returns the length measurement of the boundary of an ST_Surface or ST_MultiSurface value. (Polygon, Multipolygon)
#
# ```sql
# SELECT ST_Perimeter('POLYGON((0 0, 4 0, 4 4, 0 4, 0 0))'::geometry);
# -- result
# 16
# ```
#
# ## ST_SRID(geometry g1) => integer
#
# - [ST_SRID](http://postgis.net/docs/ST_SRID.html): Returns the spatial reference identifier for the ST_Geometry as defined in spatial_ref_sys table.
#
# ```sql
# SELECT ST_SRID(ST_GeomFromText('POINT(1 2)', 4326));
# -- result
# 4326
# ```
#
# ## ST_StartPoint(geometry g1) => geometry
#
# - [ST_StartPoint](http://postgis.net/docs/ST_StartPoint.html): Returns the first point of a LINESTRING geometry as a POINT.
#
# ```sql
# SELECT ST_StartPoint('LINESTRING(0 0, 1 1, 2 2)'::geometry);
# -- result
# POINT(0 0)
# ```


