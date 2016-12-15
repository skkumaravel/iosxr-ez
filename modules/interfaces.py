from grpc.framework.interfaces.face.face import AbortionError
import json
import copy
from collections import OrderedDict

def get_interfaces(driver):
    '''Speed is missing'''

    interfaces = {}

    INTERFACE_DEFAULTS = {
        'is_enabled': False,
        'is_up': False,
        'mac_address': u'',
        'description': u'',
        'speed': -1,
        'last_flapped': -1.0
    }

    try:
        err, interface_json = driver.getoper('{"openconfig-interfaces:interfaces": [null]}')
        if err:
            return err
    except AbortionError:
        return 'Unable to connect to local box, check your gRPC destination.'

    interface_json = json.loads(interface_json, object_pairs_hook=OrderedDict)
    interfaces_json = interface_json["openconfig-interfaces:interfaces"]['interface']

    for interface in interfaces_json:
        interface_name = interface['name']
        if interface_name != 'Null0':
            enabled = interface['state']['enabled']
            if interface['state']['oper-status'] == 'UP':
                is_up = True
            mac_address = interface['openconfig-if-ethernet:ethernet']['state']['hw-mac-address']
            description = interface['state']['description']
            last_flapped = interface['state']['last-change']
            interfaces[interface_name] = copy.deepcopy(INTERFACE_DEFAULTS)
            interfaces[interface_name].update({
                'is_up': is_up,
                'last_flapped': last_flapped,
                'is_enabled': enabled,
                'mac_address': mac_address,
                'description': description
            })

    return interfaces

def get_interfaces_counters(driver):

    interface_counters = {}
    try:
        err, interface_json = driver.getoper('{"openconfig-interfaces:interfaces": [null]}')
        if err:
            return err
    except AbortionError:
        return 'Unable to connect to local box, check your gRPC destination.'
    translate = {
        'out-multicast-pkts':'tx_multicast_packets',
        'out-unicast-pkts': 'tx_unicast_packets',
        'out-broadcast-pkts': 'tx_broadcast_packets',
        'out-discards': 'tx_discards',
        'out-octets': 'tx_octets',
        'out-errors': 'tx_discards',
        'in-multicast-pkts': 'rx_multicast_packets',
        'in-unicast-pkts': 'rx_unicast_packets',
        'in-broadcast-pkts': 'rx_broadcast_packets',
        'in-discards': 'rx_discards',
        'in-octets': 'rx_octets',
        'in-errors': 'rx_errors'
    }

    interface_json = json.loads(interface_json, object_pairs_hook=OrderedDict)
    interfaces_json = interface_json["openconfig-interfaces:interfaces"]['interface']
    for interface in interfaces_json:
        interface_name = interface['name']
        interface_stats = {}
        if interface_name != 'Null0':
            counters = interface['state']['counters']
            for counter in counters.keys():
                if counter in translate:
                    print counter
                    interface_stats[translate[counter]] = counters[counter]
            interface_counters[interface_name] = interface_stats

    return interface_counters

def get_interfaces_ip(driver):
    interfaces_ip = {}
    try:
        err, interface_json = driver.getconfig('{"openconfig-interfaces:interfaces": [null]}')
        if err:
            return err
    except AbortionError:
        return 'Unable to connect to local box, check your gRPC destination.'

    interface_json = json.loads(interface_json, object_pairs_hook=OrderedDict)
    interfaces_json = interface_json["openconfig-interfaces:interfaces"]['interface']
    for interface in interfaces_json:
        interface_name = interface['name']
        if 'subinterfaces' in interface:
            if interface_name not in interfaces_ip.keys():
                interfaces_ip[interface_name] = {}
            for index in interface['subinterfaces']['subinterface']:
                if 'openconfig-if-ip:ipv4' in index:
                    interfaces_ip[interface_name]['ipv4'] = {}
                    for address in index['openconfig-if-ip:ipv4']['address']:
                        ip = address['ip']
                        interfaces_ip[interface_name]['ipv4'][ip] = {}
                        interfaces_ip[interface_name]['ipv4'][ip]['prefix_length'] = address['config']['prefix-length']
                if 'openconfig-if-ip:ipv6' in index:
                    interfaces_ip[interface_name]['ipv6'] = {}
                    for address in index['openconfig-if-ip:ipv4']['address']:
                        ip = address['ip']
                        interfaces_ip[interface_name]['ipv6'][ip] = {}
                        interfaces_ip[interface_name]['ipv6'][ip]['prefix_length'] = address['config']['prefix-length']
    return interfaces_ip
