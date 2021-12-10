#!/bin/sh

local_ip=$1
start_port=$2
server_ip_port=$3
db_name=$4

echo $local_ip
echo $start_port
echo $server_ip_port
echo $db_name

count=`find config/ -name ${local_ip}* |wc -l`

echo $count

rm -rf /tmp/p2ptest-agent*log

index=0
while(( $index<$count ))
do
    echo $index
    act_port=`expr $index + $start_port`
    nohup ./p2ptest-agent -f /tmp/p2p_test/log/$index/xtop.log -a $server_ip_port -d $db_name -p $act_port --nodaemon &
    let "index++"
done
