# Copyright 2012 OpenStack LLC.
# All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the spec

#import json
import logging
import unittest
#import contextlib
#from webob import exc
#import netaddr

import mock
import webtest

from quantum.api.v2 import router
#from quantum.tests.unit.testlib_api import create_request
#from quantum.wsgi import Serializer, XMLDeserializer, JSONDeserializer
#from quantum.wsgi import Serializer, JSONDeserializer


LOG = logging.getLogger(__name__)


def _get_path(resource, id=None, fmt=None):
    path = '/%s' % resource

    if id is not None:
        path = path + '/%s' % id

    if fmt is not None:
        path = path + '.%s' % fmt

    return path


class APIv2TestCase(unittest.TestCase):
    # NOTE(jkoelker) This potentially leaks the mock object if the setUp
    #                raises without being caught. Using unittest2
    #                or dropping 2.6 support so we can use addCleanup
    #                will get around this.
    def setUp(self):
        # NOTE(jkoelker) No need to call super() since
        #                unittest.TestCase.setUp is just a `pass` statement
        plugin = 'quantum.quantum_plugin_base_v2.QuantumPluginBaseV2'
        self._plugin_patcher = mock.patch(plugin, autospec=True)
        self.plugin = self._plugin_patcher.start()

        api = router.APIRouter({'plugin_provider': plugin})
        self.api = webtest.TestApp(api)

    def tearDown(self):
        # NOTE(jkoelker) No need to call super() since
        #                unittest.TestCase.tearDown is just a `pass`
        #                statement
        self._plugin_patcher.stop()
        self.api = None
        self.plugin = None

    def _req(self, method, resource, data=None, fmt=None,
             content_type=None, id=None):
        pass

    def test_create_network_fmt_json(self):
        data = {'network': {'name': 'beavis', 'admin_state_up': True}}
        instance = self.plugin.return_value
        instance.create_network.return_value = data['network']
        res = self.api.post_json(_get_path('networks'), data)
        LOG.debug(res.status)
        LOG.debug(res.json)
        raise Exception
