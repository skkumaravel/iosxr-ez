from grpc.framework.interfaces.face.face import AbortionError
import json
from collections import OrderedDict

def get_arp_table(self):
    arp_table = []
    try:
        err, arp_json = self.driver.getoper('{"Cisco-IOS-XR-ipv4-arp-oper:arp": [null]}')
        if err:
            return err
    except AbortionError:
        return 'Unable to connect to local box, check your gRPC destination.'
    arp_json = json.loads(arp_json, object_pairs_hook=OrderedDict)
    for node in  arp_json["Cisco-IOS-XR-ipv4-arp-oper:arp"]['nodes']['node']:
        for entry in node['entries']['entry']:
            if 'age' in entry:
                age = entry['age']
            else:
                age = 0
            arp_table.append(
                    {
                        'interface' : entry['interface-name'],
                        'mac' : entry['hardware-address'],
                        'ip' : entry['address'],
                        'age' : age
                    }
                )
    return arp_table

def get_mac_address_table(driver):
    """ need l2 address to make this work"""
    pass
