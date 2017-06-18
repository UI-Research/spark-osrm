#!/bin/bash

sudo yum update -y
sudo yum install docker curl postgresql-libs python-psycopg2 -y
sudo service docker start
aname=north-america-latest
for i in .osrm .osrm.cnbg .osrm.cnbg_to_ebg .osrm.core .osrm.datasource_names .osrm.ebg .osrm.ebg_nodes .osrm.edges .osrm.enw .osrm.fileIndex .osrm.geometry .osrm.hsgr .osrm.icd .osrm.level .osrm.names .osrm.nbg_nodes .osrm.properties .osrm.ramIndex .osrm.restrictions .osrm.timestamp .osrm.tld .osrm.tls .osrm.turn_duration_penalties .osrm.turn_penalties_index .osrm.turn_weight_penalties; do
sudo curl https://YOUR S3 BUCKET HERE/${aname}${i} -o /mnt/${i}
done
sudo curl https://jdbc.postgresql.org/download/postgresql-9.4.1212.jre6.jar -o /mnt/postgresql-9.4.1212.jre6.jar
sudo cp -r /usr/lib64/python2.6/dist-packages/psycopg2 /usr/lib64/python2.7/dist-packages/psycopg2
sudo chmod 755 /mnt/${aname}.osrm*
sudo docker run -itd -p 5000:5000 -v /mnt:/data --name osrm-container osrm/osrm-backend osrm-routed /data/${aname}.osrm