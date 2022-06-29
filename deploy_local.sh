#!/bin/bash

#kill
ps -ef | grep xelect_net_demo | grep -v grep | awk -F ' ' '{print $2}' | xargs kill -9

tar -zxvf downloads/xelect_net_demo_dbg.tar.gz -C downloads/

mkdir -p local
rm -rf ./local/*
mkdir -p local/log
mkdir -p local/db

# mkdir logs
find config/all/ -name "127.0.0.1*" | awk -F '_' '{print $2}' | awk -F '.' '{print $1}' |xargs -I dcnt sh -c 'mkdir -p ./local/log/dcnt'
find config/all/ -name "127.0.0.1*" | awk -F '_' '{print $2}' | awk -F '.' '{print $1}' |xargs -I dcnt sh -c 'touch ./local/log/dcnt/xtop.log'

# mkdir dbs
find config/all/ -name "127.0.0.1*" | awk -F '_' '{print $2}' | awk -F '.' '{print $1}' |xargs -I dcnt sh -c 'mkdir -p ./local/db/dcnt'

# cp demo exe
cp ./downloads/xelect_net_demo ./local/
# cp debug if need comments above and uncomments the next line
# cp ./downloads/xelect_net_demo_dbg ./local/xelect_net_demo
cp ./config/all ./local/config -r 
cp ./config/all_node_info.json ./local/config/

sleep 0.5

cd local

find config/ -name "127.0.0.1*" | xargs -I conf sh -c './xelect_net_demo -c conf -g 0 &'