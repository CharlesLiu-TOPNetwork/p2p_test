## p2p test deploy tools

### preparation:
* ansible **host** file, put it in `config` directory. NOTED: rename it to `host`
* change `./config/static_network_config` file, depends on what the net size that you want to build.
* RUN commands:
``` BASH
rm -rf config/all*
./downloads/xelect_net_demo -c ./config/static_network.config -x
python3 update_config.py -i true -m 8
# -m means how may nodes in every machine.
# m * len(host) = len(address)

```
### build net:
``` BASH
python3 scripts/ansible_files.py config/host
python3 scripts/ansible_start.py config/host
```


### start agent:
``` BASH
python3 scripts/ansible_agent_start.py config/host
```

### send command:
``` BASH
# todo
```

### stop:
``` BASH
python3 scripts/ansible_stop.py config/host
```
### NOTED:
* The `xelect_net_demo` , aka `p2p test demo`, use port 9126 as communication port, and port 10125 as grpc port (to recv commands)
* IF every nodes runs more than one demo, than it will use `9126 + delta`, `10125 + delta` port , delta range from `0` to `n - 1`