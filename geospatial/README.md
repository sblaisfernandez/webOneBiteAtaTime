# Refresher Geodetic and cartographic projection for North America, Canada, Quebec

## Geoid

The geed is the shape that the ocean surface will take under the influence of the gravity of the Earth, including gravitational attraction and earth rotation.

## Geodetic reference datum or geodetic reference system

 JOD tech reference system is a reference frame for a mathematical representation of a position on the earth. Coordinate system can be planimetric, Vertical or geocentric coordinates.

The ellipsoid of revolution is often used as a mathematical model to represent the earth.

- North American Datum (NAD) 1927 using the Clarke 1866 spheroid
- NAD 1983 using the Geodetic Reference System (GRS) 1980 spheroid
- World Geodetic System (WGS) 1984 using the WGS 1984 spheroid

### North American Datum - NAD83(CSRS)

- [NAD27 -> EPSG:4267](https://epsg.io/4267)
- [NAD83 -> EPSG:4269](https://epsg.io/4269)

## Canadian Spatial Reference System: CSRS

There are two datums used in Canada: the North American Datum of 1927 (NAD27) and the North American Datum of 1983 (NAD83). Both are geodetic reference systems, but each is based on different measurements and reference ellipsoids. The NAD27 is based on the Clarke ellipsoid of 1866, and its reference point is a fixed point in Kansas. The NAD83 is an earth-centred datum based on a newly defined ellipsoid – the Geodetic Reference System of 1980 (GRS80) – and its reference point is the centre of the earth, as opposed to a point on the earth's surface.

- [NAD83(CSRS) -> EPSG:4617](https://epsg.io/4617)
- [CSRS](https://natural-resources.canada.ca/maps-tools-and-publications/geodetic-reference-systems/canadian-spatial-reference-system-csrs/9052)

## World Geodetic System 1984 (WGS84)

Use for the Global position system (GPS) provide latitude and longitude.

- [WGS84 -> EPSG:4326](https://epsg.io/4326)

## Altimetric system in Quebec

- [Réseau géodésique du Québec](https://mrnf.gouv.qc.ca/repertoire-geographique/reseau-geodesique-points-geodesiques/)

### Canadian Geodetic Vertical Datum of 2013

- [CGVD2013 -> EPSG:1127](https://epsg.io/1127)

### Canadian Geodetic Vertical Datum of 1928

- [CGVD28 -> EPSG:5114](https://epsg.io/5114-datum)

## Map projections

Map projections refer to the methods and procedures used to transform the spherical three-dimensional earth into two-dimensional planar surfaces.

These surfaces are the plane, the cylinder, and the cone.

### Equidistant projections

Map projections that accurately represent distances are referred to as equidistant projections.
Note that distances are only correct in one direction, usually north-south, and are not correct across the map.

### Conformal projections

Maps that represent angles between locations also referred to as bearings are called conformal. Conformal map projections maintain a bearing or head when traveling great distances. However, the cost of preserving bearings is that areas tend to be quite distorted in conformal map projections.
The Mercator projection is an example of a conformal projection and is famous for distorting Greenland.

### Equivalent projections

As the name indicates, equal area or equivalent projections preserve the area’s quality. Such projections are particularly useful when accurate measures or comparisons of geographical distributions are necessary (e.g., deforestation, wetlands) Moreover, such projections distort distances as well as angular relationships.

- [Map Projections](https://slcc.pressbooks.pub/maps/chapter/2-3/)

## What are the most use cartographique projection in Quebec and in Canada ?

### Canada

#### Universal Transverse Mercator (UTM) Projection

**The Canada Centre for Mapping and Earth Observation (CCMEO)** uses the Universal Transverse Mercator (UTM) Projection for mapping of the National Topographic System (NTS) series at 1:50 000 and 1:250 000 scales. [UTM Grid](https://natural-resources.canada.ca/earth-sciences/geography/topographic-information/maps/utm-grid-map-projections/utm-grid-universal-transverse-mercator-projection/9779)

The globe is 360° in circumference, a division into sixty vertical zones gives each zone the width of 6° of longitude. By international usage these zones have been numbered 1 to 60. Sixteen of the zones, bearing numbers 7 to 22, cover Canada.

![UTM zones](https://natural-resources.canada.ca/sites/nrcan/files/earthsciences/images/topo101/images/utm_figure2_en.gif)

#### The Lambert conformal conic projection

**Statistic Canada** use the Lambert conformal conic projection provides good directional and shape relationships for mid-latitude regions having a mainly east-to-west extent. Standard parallels at 49° N and 77° N are most commonly used. The scale is correct along the standard parallels only; areal deformation decreases between and increases away from the standard parallels. The central meridian, normally at 91° 52' W, is a straight line about which the projection is symmetrical. False eastings and northings are given to ensure positive coordinate values in linear units of measure (metres).

Canada spans UTM zones 7 to 22. Each UTM zone has its own EPSG code, which follows the pattern EPSG:326XX

- [UTM Zone 7N: EPSG:32607](https://epsg.io/32607)
- [UTM Zone 22N: EPSG:32622](https://epsg.io/32622)

![The Lambert conformal conic projection](https://www150.statcan.gc.ca/n1/pub/92-195-x/2011001/other-autre/mapproj-projcarte/images/fig14-eng.jpg)

- [The lanbert conformal conic projection => EPSG:3347](https://epsg.io/3347)
- [Spatial Reference EPSG:3347](https://spatialreference.org/ref/epsg/3347/)
- [EPSG:3348](https://epsg.io/3348)

The Lambert conformal conic projection by Statistics Canada for the Census data.

### Quebec

Système de coordonnées planes du Québec (SCOPQ):

- [Spatial Reference EPSG:2013](https://spatialreference.org/ref/epsg/2013/)


