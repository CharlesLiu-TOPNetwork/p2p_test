import os
import sys

def usage():
    print("python3 ansible_start.py host_file_path")


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

    cmd = "ansible -i {0} all -m shell -a \"cd /tmp/p2p_test/ && nohup python3 start.py\"".format(
        host_file)
    print(cmd)
    os.system(cmd)