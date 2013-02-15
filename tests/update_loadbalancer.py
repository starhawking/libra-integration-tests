# Copyright 2012 Hewlett-Packard Development Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

""" create_loadbalancer
    e2e tests for creating loadbalancers via atlas lbaas

"""

import ast
import unittest
import requests

import lbaas_utils

class testUpdateLoadBalancer(unittest.TestCase):

    def __init__( self, test_description, args, logging, driver
                , testname, lb_name, nodes, update_data, lb_id=None
                , algorithm = None, expected_status=200
                , backend_nodes = None):
        super(testUpdateLoadBalancer, self).__init__(testname)
        self.test_description = test_description
        self.args = args
        self.logging = logging
        self.driver = driver
        self.algorithm = algorithm
        self.update_data = update_data
        self.bad_statuses = ['500','413','400']
        if type(lb_name) is int:
            self.lb_name = str(lb_name)
        else:
            self.lb_name = lb_name
        self.nodes = nodes
        self.lb_id = lb_id
        self.expected_status = expected_status
        self.backend_nodes = backend_nodes

    def report_info(self):
        """ function for dumping info on test failures """
        report_values = ['test_description', 'update_data', 'expected_status']
        msg_data = ['']
        for report_value in report_values:
            msg_data.append("%s: %s" %(report_value, getattr(self,report_value)))
        msg_data.append('')
        return '\n'.join(msg_data)

    def setUp(self):
        ###########################
        # test create load balancer
        ###########################
        print ''
        self.logging.info("Setting up for testcase:")
        report_values = ['test_description', 'update_data', 'expected_status']
        for report_value in report_values:
            self.logging.info("  - %s: %s" %(report_value, getattr(self,report_value)))
        if self.args.verbose:
            self.logging.info("name: %s" %self.lb_name)
            self.logging.info("nodes: %s" %self.nodes)    
        # Create our loadbalancer
        self.create_result, self.actual_status, self.lb_id = self.driver.create_lb(self.lb_name, self.nodes, self.algorithm, self.bad_statuses)
        if self.args.verbose:
            self.logging.info('load balancer id: %s' %self.lb_id)
            self.logging.info("")

    def test_updateLoadBalancer(self):
        """ test update of loadbalancers for libra
        """
        # update our loadbalancer
        self.update_result, self.actual_status = self.driver.update_lb(self.lb_id, self.update_data)
        if 'name' in self.update_data:
            self.lb_name = self.update_data['name']
        lbaas_utils.validate_loadBalancer(self)
        
    def tearDown(self):
        ##########################
        # delete the load balancer
        ##########################
        self.logging.info("Deleting loadbalancer: %s" %self.lb_id)
        result = self.driver.delete_lb(self.lb_id)

 
