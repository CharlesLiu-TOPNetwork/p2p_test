import os
import socket

log_base = './log'
db_base = './db'


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


def clear_log_db(log_base='./log', db_base='./db'):
    local_ip = get_local_ip()

    rmlog_cmd = 'find {0} -name xtop*.log |xargs rm -f'.format(log_base)
    print(rmlog_cmd)
    os.system(rmlog_cmd)

    mkdirlog_cmd = r"find config/ -name '" + local_ip + r"*' | awk -F '_' '{print $2}' | awk -F '.' '{print $1}' | xargs -I dcnt sh -c 'mkdir -p ./log/dcnt' "
    # mkdirlog_cmd = 'mkdir -p {0}'.format(log_base)
    os.system(mkdirlog_cmd)

    touchlog_cmd = r"find config/ -name '" + local_ip + r"*' | awk -F '_' '{print $2}' | awk -F '.' '{print $1}' | xargs -I dcnt sh -c 'touch ./log/dcnt/xtop.log' "
    # touchlog_cmd = 'touch {0}/xtop.log'.format(log_base)
    # print(touchlog_cmd)
    os.system(touchlog_cmd)

    rmdb_cmd = 'rm -rf {0}/*'.format(db_base)
    print(rmdb_cmd)
    os.system(rmdb_cmd)

    mkdirdb_cmd = r"find config/ -name '" + local_ip + r"*' | awk -F '_' '{print $2}' | awk -F '.' '{print $1}' | xargs -I dcnt sh -c 'mkdir -p ./db/dcnt' "
    # mkdirdb_cmd = 'mkdir -p {0}'.format(db_base)
    os.system(mkdirdb_cmd)


def start():
    local_ip = get_local_ip()
    # config_file = './config/all/{0}.config'.format(local_ip)
    # print("run xelect_net_demo using config:{0}".format(config_file))

    # if not os.path.exists(config_file):
    #     print('{0} not exist'.format(config_file))
    #     return False

    mkdirdb_cmd = r"find config/ -name '" + local_ip + r"*' | xargs -I conf sh -c './xelect_net_demo -c conf -g 0 & ' "
    # cmd = './xelect_net_demo -c {0} -g 0 &'.format(config_file)
    print(mkdirdb_cmd)
    os.system(mkdirdb_cmd)
    return True


if __name__ == "__main__":
    clear_log_db()
    start()
