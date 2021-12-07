#!/usr/bin/env python
#-*- coding:utf8 -*-

import os
import json
import sys
import socket
import time
import argparse
import pdb


config_file = "./config/demo.conf"
# run_mode = ''

demo_path = "./downloads/xelect_net_demo"


def mkconf(path):
    if not os.path.exists(path):
        os.makedirs(path)
    return

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '0.0.0.0'
    finally:
        s.close()
    return IP

def dump_field(name, fout = None, field = {}):
    if not field or not fout:
        return
    field_str = "[{0}]\n".format(name)
    fout.write(field_str)
    for (k,v) in field.items():
        line = "{0} = {1}\n".format(k, v)
        fout.write(line)
    fout.write("\n")

def load_all_host(filename = "./host"):
    ip_list = []
    if not os.path.exists(filename):
        print("{0} not exist".format(filename))
        return ip_list
    with open(filename , 'r') as fin:
        for line in fin:
            if line.find('ansible_ssh_user=') == -1:
                continue
            ip = line.split()[0]
            if ip not in ip_list:
                ip_list.append(ip)
        fin.close()
    print("get {0} nodes".format(len(ip_list)))
    return ip_list


def load_all_node_info(filename = "./all_node_info.json"):
    account_list = []
    if not os.path.exists(filename):
        print("{0} not exist".format(filename))
        return account_list
    all_info = json.loads(open(filename, 'r').read())
    #print(json.dumps(all_info, indent=4))
    account_list = all_info.get('all')
    print("account_list size {0}".format(len(account_list)))
    return account_list


def update_config(account, ip, public_endpoints):
    local_ip = get_local_ip()
    local_ip = ip
    log = {
            "path": "./log/xtop.log",
            "off": "false",
            "debug": "false",
            }

    node = {
            "first_node": "false",
            "local_ip": local_ip,
            "local_port": 9126,
            "country": "CN",
            "public_endpoints": public_endpoints,
            "show_cmd": "false",
            "node_id": account,
            }

    db = {
            "path": "./db",
            }

    elect = {
            }

    node_config_file = './config/all/{0}.config'.format(local_ip)

    with open(node_config_file, 'w') as fout:
        dump_field("log", fout, log)
        dump_field("node", fout, node)
        dump_field("db", fout, db)
        fout.close()

def generate_all_node_config():
    # global run_mode

    account_list = load_all_node_info(filename = "./config/all_node_info.json")
    # if run_mode == 'dist':
    ip_list      = load_all_host(filename = "./config/host")
    if len(ip_list) != len(account_list) or len(ip_list) == 0:
        print("ip_list.length is {0} not equal account_list:{1}, please generate all_node_info again using the right number".format(len(ip_list), len(account_list)))
        return False

    public_endpoints = '{0}:9126,{1}:9126,{2}:9126,{3}:9126'.format(ip_list[0], ip_list[1], ip_list[2], ip_list[3])
    for i in range(0, len(account_list)):
        account = account_list[i]
        ip      = ip_list[i]
        update_config(account, ip, public_endpoints)
        print("generate config for node ip:{0} ok".format(ip))

    print("generate {0} config file, saved in config/all dir".format(len(account_list)))
    return True

def check_require(static_network_config_file = "./config/static_network.config"):
    # global run_mode
    if not os.path.exists(demo_path):
        print('{0} not exist'.format(demo_path))
        return False
    cmd = '{0} -h'.format(demo_path)
    result = os.popen(cmd).readlines()

    help_work_flag = False
    for lh in result:
        if lh.find('Allowed options:') != -1:
            help_work_flag = True
            break
    if not help_work_flag:
        print("{0} can not work, please check".format(cmd))
        return False

    cmd = '{0} -c ./config/static_network.config  -x'.format(demo_path)
    if not os.path.exists(static_network_config_file):
        print("please make sure you are in proxy machine or you want to deploy distributedly")
        print("{0} not exist, please put {1} in ./config, you may refer to ./config/static_network.config.default;\n and then run command: {2} ".format(static_network_config_file, static_network_config_file, cmd))
        return False

    print("please check the parameter in {0}:".format(static_network_config_file))
    with open(static_network_config_file, 'r') as fin:
        for line in fin:
            if line[-1] == '\n':
                line = line[:-1]
            print(line)

    yesno = input('Is the parameters right for you? Please input yes(y) and no(n)')
    if yesno != 'y' and yesno != 'Y':
        return False

    cmd = '{0} -c ./config/static_network.config  -x'.format(demo_path)
    result = os.popen(cmd).readlines()
    if result[-1].find('all_node_info.json') == -1:
        print("{0} can not work, please check".format(cmd))
        return False

    # if run_mode == 'dist':
    if not os.path.exists('./config/host'):
        print('./config/host not exist for dist deploy')
        return False

    return True

def init_deploy():
    mkconf('./config')
    mkconf('./config/all')
    mkconf('./log')

    static_network_config_file = "./config/static_network.config"
    if check_require(static_network_config_file = static_network_config_file):
        generate_all_node_config()
    return


def run_xelect_net_demo_one(config_file, background = True):
    node_config_file = config_file
    if not os.path.exists(node_config_file):
        print('{0} not exist'.format(node_config_file))
        return False

    if background:
        cmd = '{0} -c {1} -g 0 &'.format(demo_path, node_config_file)
        print(cmd)
        os.system(cmd)
    else:
        cmd = '{0} -c {1}'.format(demo_path,node_config_file)
        print(cmd)
        os.system(cmd)
    return True

def kill_xelect_net_demo():
    cmd = "kill -9 `ps -ef |grep xelect_net_demo |grep -v grep |awk -F ' ' '{print $2}'` "
    print(cmd)
    os.system(cmd)
    print("kill all xelect_net_demo done")
    return True

def clear_log_db(log_base = './log', db_base = './db'):
    rmlog_cmd = 'find {0} -name *.log |xargs rm -f'.format(log_base)
    print(rmlog_cmd)
    os.system(rmlog_cmd)

    for db_path in os.listdir(db_base):
        db_path = os.path.join(db_base, db_path)
        rmdb_cmd = 'rm -rf {0}/*'.format(db_path)
        print(rmdb_cmd)
        os.system(rmdb_cmd)

def run_xelect_net_demo():
    # global run_mode

    clear_log_db()

    # if run_mode == 'dist':
    local_ip = get_local_ip()
    config_file = './config/all/{0}.config'.format(local_ip)
    print("run xelect_net_demo using config:{0}".format(config_file))
    return run_xelect_net_demo_one(config_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.description='xelect_net_demo 运维工具，支持根据 host 文件生成所有节点的 config 文件；支持启动、终止、重启 xelect_net_demo 等'
    # parser.add_argument('-m',   '--mode',      type=str,  help='run mode: cent[ral] for deploy multi-nodes in local-machine; dist[ributed] for deploy multi-nodes in distributed-machines', choices = ['cent', 'dist'], required=True)
    parser.add_argument('-i',   '--init',      type=str,  help='only using this in proxy-host(jump-host) to generate all config files', default='false')
    parser.add_argument('-s',   '--start',     type=str,  help="start xelect_net_demo", default='false')
    parser.add_argument('-r',   '--restart',   type=str,  help="restart xelect_net_demo", default='false')
    parser.add_argument('-k',   '--kill',      type=str,  help="kill   xelect_net_demo", default='false')
    args = parser.parse_args()

    # if args.mode == 'dist':  # run in dist mode
    #     run_mode = 'dist'
    # elif args.mode == 'cent': # run in central mode
    #     run_mode = 'cent'
    # else:
    #     print("run_mode must in [dist, cent]")
    #     sys.exit(-1)

    if args.init == 'true':
        #just run in proxy machine
        init_deploy()
        sys.exit(0)

    if args.start == 'true':
        # run in real node 
        run_xelect_net_demo()
        sys.exit(0)

    if args.restart == 'true':
        kill_xelect_net_demo()
        run_xelect_net_demo()
        sys.exit(0)

    if args.kill  == 'true':
        kill_xelect_net_demo()
        sys.exit(0)

    print("invalid parameters, using -h to see help info")
    sys.exit(-1)
