import os
import sys

from scripts import config as cconfig

def usage():
    print("python3 ansible_agent_start.py host_file_path")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage()
        exit(-1)
    host_file = sys.argv[1]
    print("using host file {0}".format(host_file))

    print("")
    print(
        "make sure you have distrub config files use: python3 ansible_files.py!"
    )
    print("")
    yesno = input('input y to continue: ')
    if yesno != 'y' and yesno != 'Y':
        sys.exit(-1)

    cmd = "ansible -i {0} all -m shell -a \"cd /tmp/p2p_test/agent/ && python3 main.py -f /tmp/p2p_test/log/xtop.log -a {1} \"".format(
        host_file, cconfig.TOP_DW_IP_PORT)
    print(cmd)
    os.system(cmd)
