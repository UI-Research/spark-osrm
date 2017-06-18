#!/bin/bash

sudo apt-get update -y
sudo apt-get install build-essential git cmake pkg-config \
libbz2-dev libstxxl-dev libstxxl1v5 libxml2-dev \
libzip-dev libboost-all-dev lua5.2 liblua5.2-dev libtbb-dev git curl python-pip python-dev -y
sudo pip install --upgrade pip 
sudo pip install --upgrade virtualenv 
sudo pip install --upgrade --user awscli
git clone https://github.com/Project-OSRM/osrm-backend.git
curl -O http://download.geofabrik.de/north-america-latest.osm.pbf
cd osrm-backend

mkdir -p build
cd build
cmake ..
cmake --build .
sudo cmake --build . --target install

sudo su
bash -c "echo disk=/opt/.stxxl,100000,memory" > /opt/.stxxl
cd /opt