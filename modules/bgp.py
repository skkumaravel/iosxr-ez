from grpc.framework.interfaces.face.face import AbortionError
import json
from collections import OrderedDict

def get_bgp_neighbors(driver):

    neighbors = {}
    try:
        err, bgp_neighbors_json = driver.getoper('{"openconfig-bgp:bgp": [null]}')
        if err:
            return err
    except AbortionError:
        return 'Unable to connect to local box, check your gRPC destination.'

    bgp_neighbors_json = json.loads(bgp_neighbors_json, object_pairs_hook=OrderedDict)
    bgp = bgp_neighbors_json['openconfig-bgp:bgp']
    neighbors_json = bgp['neighbors']['neighbor']
    for neighbor in neighbors_json:
        this_neighbor = {}
        this_neighbor['local_as'] = bgp['global']['state']['as']
        this_neighbor['remote_id'] = neighbor['neighbor-address']
        neighbor_ip = neighbor['transport']['state']['remote-address']
        if 'peer-group' in neighbor['state']:
            peer_group = neighbor['state']['peer-group']
            peer_groups = bgp['peer-groups']['peer-group']
            peer = (item for item in peer_groups if peer_group == item['peer-group-name']).next()
            this_neighbor['remote_as'] = peer['state']['peer-as']
        else:
            this_neighbor['remote_as'] = neighbor['state']['peer-as']
#                if all(ip['state']['active'] for ip in neighbor['afi-safis']['afi-safi']):
#                    this_neighbor['is_enabled'] = True
#                else:
#                    this_neighbor['is_enabled'] = False
#               this_neighbor['description']
        this_neighbor['is_enabled'] = True #defaulting this for now
        if neighbor['state']['session-state'] == 'bgp-st-estab':
            this_neighbor['is_up'] = True
            #this_neighbor['uptime'] = -1
        else:
            this_neighbor['is_up'] = False
        for ip in neighbor['afi-safis']['afi-safi']:
            this_neighbor['address_family'] = {}
            if 'ipv4' in ip['afi-safi-name']:
                this_afi = 'ipv4'
            elif 'ipv6' in ip['afi-safi-name']:
                this_afi = 'ipv6'
            this_neighbor['address_family'][this_afi] = {}
            this_neighbor['address_family'][this_afi]['received_prefixes'] = ip['state']['prefixes']['received']
            this_neighbor['address_family'][this_afi]['sent_prefixes'] = ip['state']['prefixes']['sent']
            #this_neighbor['address_family'][this_afi]['accepted_prefixes']
        neighbors[neighbor_ip] = this_neighbor

    return neighbors

def get_bgp_config(driver, group='', neighbor = ''):
    ''' To be done: Add support for non bgp_groups set up'''

    bgp_config = {}
    try:
        err, bgp_json = driver.getconfig('{"openconfig-bgp:bgp": [null]}')
        if err:
            return err
    except AbortionError:
        return 'Unable to connect to local box, check your gRPC destination.'
    bgp_json = json.loads(bgp_json, object_pairs_hook=OrderedDict)
    bgp_json = bgp_json['openconfig-bgp:bgp']
    default = {}
    default['local_as'] = bgp_json['global']['config']['as']
    default['local_address'] = bgp_json['global']['config']['router-id']
    for afi in bgp_json['global']['afi-safis']['afi-safi']:
        afi_name = afi['afi-safi-name']
        default[afi_name] = {}
        if 'use-multiple-paths' in afi:
            default[afi_name]['multipath'] = True
        else:
            default[afi_name]['multipath'] = False
    bgp_group_neighbors = {}
    for neighbor in bgp_json['neighbors']['neighbor']:
        peer = neighbor['config']['neighbor-address']
        if 'peer-group' in neighbor['config']:
            group_name = neighbor['config']['peer-group']
            if group_name not in bgp_group_neighbors.keys():
                bgp_group_neighbors[group_name] = {}
            bgp_group_neighbors[group_name][peer] = {}
    if 'peer-groups' in bgp_json:
        for bgp_group in bgp_json['peer-groups']['peer-group']:
            group_name = bgp_group['peer-group-name']
            bgp_type = 'external' #must check
            peer_as = bgp_group['config']['peer-as']
            #description =
            for afi in bgp_group['afi-safis']['afi-safi']:
                import_policy = afi['apply-policy']['config']['import-policy']
                export_policy = afi['apply-policy']['config']['export-policy']
            multipath = default[afi['afi-safi-name']]
            local_as = default['local_as']
            local_address = default['local_address']
            remote_private = True
            bgp_config[group_name] = {
                'apply_groups' : [],
                'description' : '',
                'local_as' : local_as,
                'type' : unicode(bgp_type),
                'import_policy' : import_policy,
                'export_policy' : export_policy,
                'local_address' : local_address,
                'multipath' : multipath,
                'multihop_ttl' : '',
                'remote_as': peer_as,
                'remove_private_as': remote_private,
                'prefix_limit' : '',#to build
                'neighbors' : bgp_group_neighbors.get(group_name, {})
            }

    return bgp_config
