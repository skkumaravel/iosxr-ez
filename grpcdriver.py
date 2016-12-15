# Copyright 2016 Cisco Systems All rights reserved.
#
# The contents of this file are licensed under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with the
# License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

"""
Main Module for Napalm integration with gRPC for IO-XR
"""
from util.lib.cisco_grpc_client import CiscoGRPCClient
from grpc.framework.interfaces.face.face import AbortionError
import json
import copy
from collections import OrderedDict

import modules.bgp
import modules.interfaces
import modules.lldp
import modules.ntp
import modules.tables
import modules.platform

class gRPCDriver():
    """
    This is a IOS-XR gRPC Driver for Napalm
    """
    def __init__(self, hostname, username, password, port, timeout=10):
        """
        Pulls in data for gRPC object
        """
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port
        self.timeout = timeout

    def open(self):
        """
        gRPC object created
        """
        try:
            self.driver = CiscoGRPCClient(
                self.hostname,
                self.port,
                self.timeout,
                self.username,
                self.password)
        except ValueError as conn_err:
            raise conn_err

    def get_facts(self):
        return modules.platform.get_facts(self.driver)

    def get_interfaces(self):
        '''Speed is missing'''
        return modules.interfaces.get_interfaces(self.driver)

    def get_interfaces_counters(self):
        return modules.interfaces.get_interfaces_counters(self.driver)

    def get_bgp_neighbors(self):
        return modules.bgp.get_bgp_neighbors(self.driver)

    def get_environment(self):
        """Not completed"""
        pass
        #return modules.platform.get_environment(self.driver)

    def get_lldp_neighbors(self):
        return modules.lldp.get_lldp_neighbors(self.driver)

    def get_lldp_neighbors_detail(self):
        return modules.lldp.get_lldp_neighbors_detail(self.driver)

    def cli(self, commands=None):
        """Not completed"""
        pass

    def get_bgp_config(self, group='', neighbor = ''):
        ''' To be done: Add support for non bgp_groups set up'''
        return modules.bgp.get_bgp_config(self.driver, group, neighbor)

    def get_bgp_neighbors_detail(self, neighbor_address=''):
        """Not completed"""
        pass

    def get_arp_table(self):
        return modules.tables.get_arp_table(self.driver)

    def get_ntp_servers(self):
        return modules.ntp.get_ntp_servers(self.driver)

    def get_ntp_stats(self):
        return modules.ntp.get_ntp_stats(self.driver)

    def get_interfaces_ip(self):
        return modules.interfaces.get_interfaces_ip(self.driver)

    def get_mac_address_table(self):
        """Not completed"""
        pass
    def get_snmp_information(self):
        """Not completed"""
        pass
    def get_probes_config(self):
        """Not completed"""
        pass
    def get_probes_results(self):

        pass
    def traceroute(self):
        pass








