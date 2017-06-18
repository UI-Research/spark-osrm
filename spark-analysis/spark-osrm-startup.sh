#!/bin/bash

sudo yum update -y
sudo yum install docker curl -y
sudo service docker start
aname=north-america-latest
for i in .osrm .osrm.cnbg .osrm.cnbg_to_ebg .osrm.core .osrm.datasource_names .osrm.ebg .osrm.ebg_nodes .osrm.edges .osrm.enw .osrm.fileIndex .osrm.geometry .osrm.hsgr .osrm.icd .osrm.level .osrm.names .osrm.nbg_nodes .osrm.properties .osrm.ramIndex .osrm.restrictions .osrm.timestamp .osrm.tld .osrm.tls .osrm.turn_duration_penalties .osrm.turn_penalties_index .osrm.turn_weight_penalties; do
sudo curl https://YOUR S3 BUCKET HERE/${aname}${i} -o /mnt/${i}
done
sudo chmod 755 /mnt/${aname}.osrm*
sudo docker run -itd -p 5000:5000 -v /mnt:/data --name osrm-container osrm/osrm-backend osrm-routed /data/${aname}.osrm