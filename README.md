## p2p test deploy tools

### preparation:
* ansible **host** file, put it in `config` directory. NOTED: rename it to `host`
* change `./config/static_network_config` file, depends on what the net size that you want to build.
* RUN commands:
``` BASH
./downloads/xelect_net_demo -c ./config/static_network.config -x
python3 update_config.py -i true

python3 scripts/ansible_files.py config/host
```


### NOTED:
* The `xelect_net_demo` , aka `p2p test demo`, use port 9126 as communication port, and port 10125 as grpc port (to recv commands)