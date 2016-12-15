from grpc.framework.interfaces.face.face import AbortionError
import json
from collections import OrderedDict

def get_lldp_neighbors(driver):

    lldp = {}
    try:
        err, sh_lldp = driver.getoper('{"Cisco-IOS-XR-ethernet-lldp-oper:lldp": [null]}')
        if err:
            return err
    except AbortionError:
        return 'Unable to connect to local box, check your gRPC destination.'

    sh_lldp = json.loads(sh_lldp, object_pairs_hook=OrderedDict)
    lldp_nodes = sh_lldp["Cisco-IOS-XR-ethernet-lldp-oper:lldp"]['nodes']['node']
    for node in lldp_nodes:
        for neighbor in node['neighbors']['summaries']['summary']:
            local_interface = neighbor['interface-name']
            if local_interface not in lldp.keys():
                lldp[local_interface] = []
            for lldp_neighbor in neighbor['lldp-neighbor']:
                lldp[local_interface].append({
                    'hostname': lldp_neighbor['device-id'],
                    'port': lldp_neighbor['receiving-interface-name']
                    })

    return lldp

def get_lldp_neighbors_detail(driver):
    #init result dict
    lldp_neighbors = {}
    try:
        err, sh_lldp = driver.getoper('{"Cisco-IOS-XR-ethernet-lldp-oper:lldp": [null]}')
        if err:
            return err
    except AbortionError:
        return 'Unable to connect to local box, check your gRPC destination.'

    sh_lldp = json.loads(sh_lldp, object_pairs_hook=OrderedDict)
    lldp_nodes = sh_lldp["Cisco-IOS-XR-ethernet-lldp-oper:lldp"]['nodes']['node']
    for node in lldp_nodes:
        for neighbor in node['neighbors']['details']['detail']:
            interface_name = neighbor['interface-name']
            for lldp_neighbor in neighbor['lldp-neighbor']:
                parent_interface = lldp_neighbor['receiving-interface-name']
                chassis_id = lldp_neighbor['chassis-id']
                port_id = lldp_neighbor['port-id-detail']
                port_descr = lldp_neighbor['detail']['port-description']
                system_name = lldp_neighbor['detail']['system-name']
                system_descr = lldp_neighbor['detail']['system-description']
                system_capabilities = lldp_neighbor['detail']['system-capabilities']
                enabled_capabilities = lldp_neighbor['detail']['enabled-capabilities']

                if interface_name not in lldp_neighbors.keys():
                    lldp_neighbors[interface_name] = []
                lldp_neighbors[interface_name].append({
                    'parent_interface': parent_interface,
                    'remote_chassis_id': chassis_id,
                    'remote_port': port_id,
                    'remote_port_description': port_descr,
                    'remote_system_name': system_name,
                    'remote_system_description': system_descr,
                    'remote_system_capab': system_capabilities,
                    'remote_system_enable_capab':  enabled_capabilities
                })

    return lldp_neighbors
