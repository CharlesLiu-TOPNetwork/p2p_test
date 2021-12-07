import os
import sys


def usage():
    print("python3 ansible_files.py host_file_path")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage()
        exit(-1)

    host_file = sys.argv[1]
    print("using host file {0}".format(host_file))

    print("")
    print(
        "make sure you have genator config files use: python3 update_config.py!"
    )
    print("")
    yesno = input('input y to continue: ')
    if yesno != 'y' and yesno != 'Y':
        sys.exit(-1)

    cmd = "ansible -i {0} all -m shell -a \"rm -rf /tmp/p2p_test/ \"".format(
        host_file)
    print(cmd)
    os.system(cmd)

    cmd = "ansible -i {0} all -m shell -a \"mkdir -p /tmp/p2p_test \"".format(
        host_file)
    print(cmd)
    os.system(cmd)

    cmd = "ansible -i {0} all -f 6 -m copy -a \"src=./downloads/ dest=/tmp/p2p_test/ mode=0755 \"".format(
        host_file)
    print(cmd)
    os.system(cmd)

    cmd = "ansible -i {0} all -f 6 -m copy -a \"src=./config/ dest=/tmp/p2p_test/config/ \"".format(
        host_file)
    print(cmd)
    os.system(cmd)
