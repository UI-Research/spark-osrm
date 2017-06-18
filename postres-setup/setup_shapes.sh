#!/bin/bash

apt-get update -y
apt-get install wget unzip -y
geog=tract
psql -U postgres -c "CREATE TABLE ${geog} (id serial not null primary key, geoid varchar(11), lon float8, lat float8)" 
psql -U postgres -c "SELECT AddGeometryColumn ('public','${geog}','geom',4269,'MULTIPOLYGON',2);" 
for i in 01 02 04 05 06 08 09 10 11 12 13 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 44 45 46 47 48 49 50 51 53 54 55 56; do 
	j=`echo ${geog} | awk '{print toupper($0)}'` 
	k= 
	if [[ "$geog" == puma10 ]]; then j=PUMA k=10; fi 
	if [[ "$geog" == tabblock10 ]]; then j=TABBLOCK k=10; fi
	wget http://www2.census.gov/geo/tiger/TIGER2016/${j}/tl_2016_${i}_${geog}.zip -O ${i}.zip 
	unzip ${i}.zip 
	rm ${i}.zip 
	shp2pgsql -I -s 4269 -g geom tl_2016_${i}_${geog}.shp | psql -U postgres -d postgres -q 
	rm tl_2016_${i}_${geog}* 
	psql -U postgres -c "INSERT INTO ${geog} (geoid,geom) (SELECT geoid${k}, geom FROM tl_2016_${i}_${geog})" 
	psql -U postgres -c "DROP TABLE tl_2016_${i}_${geog}" 
done 
psql -U postgres -c "CREATE INDEX ${geog}_index ON ${geog} USING GIST (geom)" 
psql -U postgres -c "SELECT AddGeometryColumn ('public','${geog}','geom',4269,'MULTIPOLYGON',2);"
psql -U postgres -c "UPDATE ${geog} SET centroid = (SELECT ST_CENTROID(geom));"
psql -U postgres -c "CREATE INDEX centroid_index ON ${geog} USING GIST (centroid);"
psql -U postgres -c "UPDATE ${geog} SET lon = ST_X(centroid);"
psql -U postgres -c "UPDATE ${geog} SET lat = ST_Y(centroid);"

echo ""
echo "Creating unique distance table, this takes about 20 minutes for tracts, and longer for smaller geographies"
echo ""
psql -U postgres -c "CREATE TABLE ${geog}_within (id serial not null primary key, geoid1 varchar(11), geoid2 varchar(11), a_lon float8, a_lat float8, b_lon float8, b_lat float8);"
psql -U postgres -c "INSERT INTO ${geog}_within (geoid1, geoid2, a_lon, a_lat, b_lon, b_lat) (SELECT a.geoid as geoid1, b.geoid as geoid2, a.lon as a_lon, a.lat as a_lat, b.lon as b_lon, b.lat as b_lat FROM ${geog} a LEFT JOIN ${geog} b ON ST_DWithin(a.centroid, b.centroid, 3.0) WHERE a.geoid <= b.geoid);"

