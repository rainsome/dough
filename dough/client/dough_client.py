#!/usr/bin/env python
# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright 2012 Sina Corporation
# All Rights Reserved.
# Author: YuWei Peng <pengyuwei@gmail.com>
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import sys
import time
from md5 import md5
import json
import zmq
import urllib2
import datetime
import base64
from collections import OrderedDict

from nova import utils
from nova import flags
from nova.openstack.common import cfg
from nova import log as logging

utils.default_flagfile(filename='/etc/dough/dough.conf')
logging.setup()

api_opts = [
    cfg.StrOpt('api_host',
               default='127.0.0.1',
               help='IP address of dough API.'),
    cfg.IntOpt('api_port',
               default=8783,
               help='Port of dough api.'),
#    cfg.StrOpt('monthly_report',
#               short='m',
#               default='name1',
#               help='monthly_report.'),
    ]
    
cli_opts = [
    cfg.StrOpt('monthly_report',
               short='m',
               default='name1',
               help='monthly_report.'),
    ]

FLAGS = flags.FLAGS
FLAGS.register_cli_opts(cli_opts)
FLAGS.register_opts(api_opts)
flags.FLAGS(sys.argv)

STANDARD_PROTOCOL = {
    'method': 'query_report',
    'args': {
        'user_id': '864bbc5d23ea47799ae2a702927920e9',
        'tenant_id': '864bbc5d23ea47799ae2a702927920e9',
        'timestamp_from': '2012-03-01T00:00:00',
        'timestamp_to': '2012-03-02T00:00:00',
        }
    }

class DoughClient():

    def __init__(self):
        context = zmq.Context()
        self.socket = context.socket(zmq.REQ)
        connstr = "tcp://%(api_host)s:%(api_port)s" % FLAGS
    #        print connstr
        self.socket.connect(connstr)
        
    def invoke(self, param):
        self.socket.send_multipart (["client", "1", json.dumps(param)])
        msg_type, uuid, message = self.socket.recv_multipart()
        return json.loads(message)
    
    def query_monthly_report(self, tenant_id, time_from, time_to):
        request = STANDARD_PROTOCOL
        request["method"] = "query_monthly_report"
        request["args"]["tenant_id"] = tenant_id
        request["args"]["timestamp_from"] = time_from
        request["args"]["timestamp_to"] = time_to

        data = self.invoke(request)
        return data
        
    def query_report(self, tenant_id, time_from, time_to, period):
        request = STANDARD_PROTOCOL
        request["method"] = "query_report"
        request["args"]["tenant_id"] = tenant_id
        request["args"]["timestamp_from"] = time_from
        request["args"]["timestamp_to"] = time_to
        request["args"]["period"] = period

        data = self.invoke(request)
        return data
        
