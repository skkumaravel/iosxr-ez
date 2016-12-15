from grpc.framework.interfaces.face.face import AbortionError
import json
from collections import OrderedDict
import interfaces

def get_facts(driver):
    facts = {
        'vendor': u'Cisco',
        'os_version': u'',
        'hostname': u'',
        'uptime': -1,
        'serial_number': u'',
        'fqdn': u'',
        'model': u'',
        'interface_list': []
        }

    try:
        err, hostname_json = driver.getoper('{"Cisco-IOS-XR-shellutil-oper:system-time": [null]}')
        if err:
            return err
    except AbortionError:
        return 'Unable to connect to local box, check your gRPC destination.'

    hostname_json = json.loads(hostname_json)
    facts['hostname'] = hostname_json['Cisco-IOS-XR-shellutil-oper:system-time']['uptime']['host-name']
    facts['fqdn'] = facts['hostname']
    facts['uptime'] = hostname_json['Cisco-IOS-XR-shellutil-oper:system-time']['uptime']['uptime']

    try:
        err, platform_json = driver.getoper('{"Cisco-IOS-XR-plat-chas-invmgr-oper:platform-inventory": [null]}')
        if err:
            return err
    except AbortionError:
        return 'Unable to connect to local box, check your gRPC destination.'

    platform_json = json.loads(platform_json)
    rack_tree = platform_json['Cisco-IOS-XR-plat-chas-invmgr-oper:platform-inventory']['racks']['rack']
    chassis_attributes = rack_tree[0]['attributes']['basic-info']

    facts['model'] = chassis_attributes['model-name']
    facts['serial_number'] = chassis_attributes['serial-number']
    facts['os_version'] = chassis_attributes['software-revision']
    facts['description'] = chassis_attributes['description']
    facts['interface_list'] = interfaces.get_interfaces(driver).keys()

    return facts

def get_environment(self):
    pass
    '''
    environment_status = {}
    environment_status['fans'] = {}
    environment_status['temperature'] = {}
    environment_status['power'] = {}
    environment_status['cpu'] = {}
    environment_status['memory'] = 0.0

    #
    # Memory
    #
    try:
        err, mem_json = self.driver.getoper('{"Cisco-IOS-XR-nto-misc-oper:memory-summary": [null]}')
        if err:
            return err
    except AbortionError:
        return 'Unable to connect to local box, check your gRPC destination.'
    mem_json = json.loads(mem_json, object_pairs_hook=OrderedDict)
    for node in mem_json['nodes']['node']:

    #
    # Fans
    #


    #
    # CPU
    #
    cpu = {}
    try:
        err, cpu_json = self.driver.getoper('{"Cisco-IOS-XR-wdsysmon-fd-oper:system-monitoring": [null]}')
        if err:
            return err
    except AbortionError:
        return 'Unable to connect to local box, check your gRPC destination.'
    cpu_json = json.loads(cpu_json, object_pairs_hook=OrderedDict)
    for module in cpu_json['cpu-utilizatio']:
        this_cpu = {}
        this_cpu['%usage'] = module['total-cpu-one-minute']
        position = module['node-name']
        cpu[position] = this_cpu
    environment_status["cpu"] = cpu

    '''
