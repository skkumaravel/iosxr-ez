from grpc.framework.interfaces.face.face import AbortionError
import json
from collections import OrderedDict

def get_ntp_servers(driver):
    ntp_servers = {}
    try:
        err, ntp_json = driver.getconfig('{"Cisco-IOS-XR-ip-ntp-cfg:ntp": [null]}')
        if err:
            return err
    except AbortionError:
        return 'Unable to connect to local box, check your gRPC destination.'
    ntp_json = json.loads(ntp_json, object_pairs_hook=OrderedDict)
    for peer in ntp_json['Cisco-IOS-XR-ip-ntp-cfg:ntp']['peer-vrfs']['peer-vrf']:
        for version in peer['peer-ipv4s']['peer-ipv4']:
            server_address = version['address-ipv4']
            for peer_type in version['peer-type-ipv4']:
                if peer_type['peer-type'] == 'server':
                    ntp_servers[server_address] = {}
    return ntp_servers

def get_ntp_stats(driver):

    ntp_stats = []

    try:
        err, ntp_json = driver.getoper('{"Cisco-IOS-XR-ip-ntp-admin-oper:ntp": [null]}')
        if err:
            return err
    except AbortionError:
        return 'Unable to connect to local box, check your gRPC destination.'
    ntp_json = json.loads(ntp_json, object_pairs_hook=OrderedDict)
    for rack in ntp_json['Cisco-IOS-XR-ip-ntp-admin-oper:ntp']['racks']['rack']:
        for slot in rack['slots']['slot']:
            for instance in slot['instances']['instance']:
                for peer_info in instance['associations']['peer-summary-info']:
                    peer_info = peer_info['peer-info-common']
                    address = peer_info['address']
                    synchronized = peer_info['is-sys-peer']
                    referenceid = peer_info['reference-id']
                    hostpoll = peer_info['host-poll']
                    reachability = peer_info['reachability']
                    stratum = peer_info['stratum']
                    delay = peer_info['delay']
                    offset = peer_info['offset']
                    jitter = peer_info['dispersion']
                    ntp_stats.append({
                        'remote' : address,
                        'synchronized' : synchronized,
                        'referenceid' : referenceid,
                        'stratum' : stratum,
                        'type' : u'',
                        'when' : u'',
                        'hostpoll' : hostpoll,
                        'reachability' : reachability,
                        'delay' : delay,
                        'offset' : offset,
                        'jitter' : jitter
                        })

    return ntp_stats
