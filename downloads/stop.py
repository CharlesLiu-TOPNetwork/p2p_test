import os

stop_cmd = "ps -ef |grep xelect_net_demo | grep -v grep |awk -F ' ' '{print $2}'|xargs kill -9"
print(stop_cmd)
os.system(stop_cmd)


stop_cmd = "ps -ef |grep p2ptest-agent | grep -v grep |awk -F ' ' '{print $2}'|xargs kill -9"
print(stop_cmd)
os.system(stop_cmd)
