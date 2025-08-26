
# GIS files format

## GeoJSON

- [The GeoJSON Format](https://datatracker.ietf.org/doc/html/rfc7946)

## TopoJSON

TopoJSON is an extension of GeoJSON that encodes topology. Rather than representing geometries discretely, geometries in TopoJSON files are stitched together from shared line segments called arcs.

- [TopoJSON](https://github.com/topojson/topojson)

## File Geodatabase (FGDB) or .gdb

File Geodatabase (FGDB) is a proprietary Esri database format, favoured for more complex uses of GIS datasets in Esri software.

File geodatabases are made up of seven system tables plus user data. User data can be stored in the following types of datasets:

Feature class
Feature dataset
Mosaic dataset
Raster catalog
Raster dataset
Schematic dataset
Table (nonspatial)
Toolboxes

Feature datasets can contain feature classes as well as the following types of datasets:

Attachments
Feature-linked annotation
Geometric networks
Network datasets
Parcel fabrics
Relationship classes
Terrains
Topologies
The default maximum size of datasets in file geodatabases is 1 TB. The maximum size can be increased to 256 TB for large datasets (usually raster).

## Well Know Text (WKT)

“Well-known text” is a scheme for writing a simple features geometry into a standard text string.

- [Well-Known Text (WKT)](https://libgeos.org/specifications/wkt/)
