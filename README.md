## p2p test deploy tools

### preparation:
* ansible **host** file, put it in `config` directory. NOTED: rename it to `host`
* edit `./config/static_network_config` file, depends on what the net size that you want to build.
* edit `./scripts/config.py` file, set the ip-port && env name 
* RUN commands and go on:
``` BASH
rm -rf config/all*
./downloads/xelect_net_demo -c ./config/static_network.config -x
python3 update_config.py -i true -m 8
# -m means how may nodes in every machine.
# m * len(host) = len(address)

```

### alternative
* use debug version to get more logs:
    * `downloads/xelect_net_demo_dbg`
    * `deploy_local.sh:20-22`
    * `update_config.py:81`: `debug:true`
* local test or remote test:
    * reference: below `### local test` and `### ansible test`

### local test

* use config/local.host.sample to generate configs
* run local shell script:

``` BASH
bash -x deploy_local.sh
```
### ansible test

##### build net:

``` BASH
python3 scripts/ansible_files.py config/host
python3 scripts/ansible_start.py config/host
```

##### start agent:

``` BASH
python3 scripts/ansible_agent_start.py config/host
```
##### stop:

``` BASH
python3 scripts/ansible_stop.py config/host
```


### send command:
based on TopPyFrame

* extend_api.py
``` PYTHON
def p2ptest(self,*args):
    remote = get_url(PROTOCOL_TYPE.GRPC)
    for item in args:
        if item.startswith("remote="):
            remote = item.split("remote=")[1]
    with mock.patch("app.app_lib.base_api.get_url", return_value=remote):
        test_cmd = args[0]
        actor = TestSeniorClient(PROTOCOL_TYPE.GRPC)
        index = 0
        if len(args) > 1:
            test_interval = args[1]
            while True:
                time_st = int(time.time()*1000)
                index = index + 1
                time.sleep(float(test_interval)/1000)
                ret = actor.p2p_test(
                    {'test_cmd': test_cmd, 'index': index})
                print('ret:\n%s' % json.dumps(ret))
                time_ed = int(time.time()*1000)
                print('actual_time: %s' % str(time_ed-time_st))
        else:
            ret = actor.p2p_test({'test_cmd': test_cmd, 'index': 0})
            print('ret:\n%s' % json.dumps(ret))
```

* base_api.py
``` PYTHON
def p2p_test(self, params={}):
    action = "p2ptest"
    body = {"action": action}
    for k in params:
        body[k] = params[k]
    return self.doPost(action=action, body=body)
```

* send_shell:
``` BASH
# print routing table
$ python3 testapp.py p2ptest "prt"
# test rrs gossip broadcast [msg_num] [msg_size] [gossip_type: 2 = rrs]
$ python3 testapp.py p2ptest "broadcast_all_new 3 199 2"
# test bloom_filter_broadcast []
$ python3 testapp.py p2ptest "broadcast_all 3 199"
```

* NOTED: remember to change env.ini ip && port


### NOTED:
* The `xelect_net_demo` , aka `p2p test demo`, use port 9126 as communication port, and port 10125 as grpc port (to recv commands)
* IF every nodes runs more than one demo, than it will use `9126 + delta`, `10125 + delta` port , delta range from `0` to `n - 1`