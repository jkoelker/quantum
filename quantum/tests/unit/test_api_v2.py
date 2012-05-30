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

import logging
import unittest

import mock
import webtest

from quantum.api.v2 import router


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

    def test_verbose_attr(self):
        instance = self.plugin.return_value
        instance.get_networks.return_value = []

        self.api.get(_get_path('networks'), {'verbose': 'foo'})
        instance.get_networks.assert_called_once_with(mock.ANY,
                                                      filters=mock.ANY,
                                                      show=mock.ANY,
                                                      verbose=['foo'])

    def test_multiple_verbose_attr(self):
        instance = self.plugin.return_value
        instance.get_networks.return_value = []

        self.api.get(_get_path('networks'), {'verbose': ['foo', 'bar']})
        instance.get_networks.assert_called_once_with(mock.ANY,
                                                      filters=mock.ANY,
                                                      show=mock.ANY,
                                                      verbose=['foo',
                                                               'bar'])

    def test_verbose_true_int(self):
        instance = self.plugin.return_value
        instance.get_networks.return_value = []

        self.api.get(_get_path('networks'), {'verbose': 1})
        instance.get_networks.assert_called_once_with(mock.ANY,
                                                      filters=mock.ANY,
                                                      show=mock.ANY,
                                                      verbose=True)

    def test_verbose_false_int(self):
        instance = self.plugin.return_value
        instance.get_networks.return_value = []

        self.api.get(_get_path('networks'), {'verbose': 0})
        instance.get_networks.assert_called_once_with(mock.ANY,
                                                      filters=mock.ANY,
                                                      show=mock.ANY,
                                                      verbose=False)

    def test_verbose_false_str(self):
        instance = self.plugin.return_value
        instance.get_networks.return_value = []

        self.api.get(_get_path('networks'), {'verbose': 'false'})
        instance.get_networks.assert_called_once_with(mock.ANY,
                                                      filters=mock.ANY,
                                                      show=mock.ANY,
                                                      verbose=False)

    def test_verbose_true_str(self):
        instance = self.plugin.return_value
        instance.get_networks.return_value = []

        self.api.get(_get_path('networks'), {'verbose': 'true'})
        instance.get_networks.assert_called_once_with(mock.ANY,
                                                      filters=mock.ANY,
                                                      show=mock.ANY,
                                                      verbose=True)

    def test_verbose_true_trump_attr(self):
        instance = self.plugin.return_value
        instance.get_networks.return_value = []

        self.api.get(_get_path('networks'), {'verbose': ['true', 'foo']})
        instance.get_networks.assert_called_once_with(mock.ANY,
                                                      filters=mock.ANY,
                                                      show=mock.ANY,
                                                      verbose=True)

    def test_verbose_false_trump_attr(self):
        instance = self.plugin.return_value
        instance.get_networks.return_value = []

        self.api.get(_get_path('networks'), {'verbose': ['false', 'foo']})
        instance.get_networks.assert_called_once_with(mock.ANY,
                                                      filters=mock.ANY,
                                                      show=mock.ANY,
                                                      verbose=False)

    def test_verbose_true_trump_false(self):
        instance = self.plugin.return_value
        instance.get_networks.return_value = []

        self.api.get(_get_path('networks'), {'verbose': ['true', 'false']})
        instance.get_networks.assert_called_once_with(mock.ANY,
                                                      filters=mock.ANY,
                                                      show=mock.ANY,
                                                      verbose=True)

    def test_show(self):
        instance = self.plugin.return_value
        instance.get_networks.return_value = []

        self.api.get(_get_path('networks'), {'show': 'foo'})
        instance.get_networks.assert_called_once_with(mock.ANY,
                                                      filters=mock.ANY,
                                                      show=['foo'],
                                                      verbose=mock.ANY)

    def test_show_multiple(self):
        instance = self.plugin.return_value
        instance.get_networks.return_value = []

        self.api.get(_get_path('networks'), {'show': ['foo', 'bar']})
        instance.get_networks.assert_called_once_with(mock.ANY,
                                                      filters=mock.ANY,
                                                      show=['foo', 'bar'],
                                                      verbose=mock.ANY)

    def test_show_multiple_with_empty(self):
        instance = self.plugin.return_value
        instance.get_networks.return_value = []

        self.api.get(_get_path('networks'), {'show': ['foo', '']})
        instance.get_networks.assert_called_once_with(mock.ANY,
                                                      filters=mock.ANY,
                                                      show=['foo'],
                                                      verbose=mock.ANY)

    def test_show_empty(self):
        instance = self.plugin.return_value
        instance.get_networks.return_value = []

        self.api.get(_get_path('networks'), {'show': ''})
        instance.get_networks.assert_called_once_with(mock.ANY,
                                                      filters=mock.ANY,
                                                      show=[],
                                                      verbose=mock.ANY)

    def test_show_multiple_empty(self):
        instance = self.plugin.return_value
        instance.get_networks.return_value = []

        self.api.get(_get_path('networks'), {'show': ['', '']})
        instance.get_networks.assert_called_once_with(mock.ANY,
                                                      filters=mock.ANY,
                                                      show=[],
                                                      verbose=mock.ANY)

    def test_filters(self):
        instance = self.plugin.return_value
        instance.get_networks.return_value = []

        self.api.get(_get_path('networks'), {'foo': 'bar'})
        filters = {'foo': ['bar']}
        instance.get_networks.assert_called_once_with(mock.ANY,
                                                      filters=filters,
                                                      show=mock.ANY,
                                                      verbose=mock.ANY)

    def test_filters_empty(self):
        instance = self.plugin.return_value
        instance.get_networks.return_value = []

        self.api.get(_get_path('networks'), {'foo': ''})
        filters = {}
        instance.get_networks.assert_called_once_with(mock.ANY,
                                                      filters=filters,
                                                      show=mock.ANY,
                                                      verbose=mock.ANY)

    def test_filters_multiple_empty(self):
        instance = self.plugin.return_value
        instance.get_networks.return_value = []

        self.api.get(_get_path('networks'), {'foo': ['', '']})
        filters = {}
        instance.get_networks.assert_called_once_with(mock.ANY,
                                                      filters=filters,
                                                      show=mock.ANY,
                                                      verbose=mock.ANY)

    def test_filters_multiple_with_empty(self):
        instance = self.plugin.return_value
        instance.get_networks.return_value = []

        self.api.get(_get_path('networks'), {'foo': ['bar', '']})
        filters = {'foo': ['bar']}
        instance.get_networks.assert_called_once_with(mock.ANY,
                                                      filters=filters,
                                                      show=mock.ANY,
                                                      verbose=mock.ANY)

    def test_filters_multiple_values(self):
        instance = self.plugin.return_value
        instance.get_networks.return_value = []

        self.api.get(_get_path('networks'), {'foo': ['bar', 'bar2']})
        filters = {'foo': ['bar', 'bar2']}
        instance.get_networks.assert_called_once_with(mock.ANY,
                                                      filters=filters,
                                                      show=mock.ANY,
                                                      verbose=mock.ANY)

    def test_filters_multiple(self):
        instance = self.plugin.return_value
        instance.get_networks.return_value = []

        self.api.get(_get_path('networks'), {'foo': 'bar',
                                             'foo2': 'bar2'})
        filters = {'foo': ['bar'], 'foo2': ['bar2']}
        instance.get_networks.assert_called_once_with(mock.ANY,
                                                      filters=filters,
                                                      show=mock.ANY,
                                                      verbose=mock.ANY)

    def test_filters_with_show(self):
        instance = self.plugin.return_value
        instance.get_networks.return_value = []

        self.api.get(_get_path('networks'), {'foo': 'bar', 'show': 'foo'})
        filters = {'foo': ['bar']}
        instance.get_networks.assert_called_once_with(mock.ANY,
                                                      filters=filters,
                                                      show=['foo'],
                                                      verbose=mock.ANY)

    def test_filters_with_verbose(self):
        instance = self.plugin.return_value
        instance.get_networks.return_value = []

        self.api.get(_get_path('networks'), {'foo': 'bar', 'verbose': 1})
        filters = {'foo': ['bar']}
        instance.get_networks.assert_called_once_with(mock.ANY,
                                                      filters=filters,
                                                      show=mock.ANY,
                                                      verbose=True)

    def test_filters_with_show_and_verbose(self):
        instance = self.plugin.return_value
        instance.get_networks.return_value = []

        self.api.get(_get_path('networks'), {'foo': 'bar',
                                             'show': 'foo',
                                             'verbose': 1})
        filters = {'foo': ['bar']}
        instance.get_networks.assert_called_once_with(mock.ANY,
                                                      filters=filters,
                                                      show=['foo'],
                                                      verbose=True)


class JSONNetworkV2TestCase(APIv2TestCase):
    def test_list_networks(self):
        return_value = [{'network': {'name': 'net1',
                                     'admin_state_up': True,
                                     'subnets': [],
                                     'tags': []}}]
        instance = self.plugin.return_value
        instance.get_networks.return_value = return_value

        res = self.api.get(_get_path('networks'))
        self.assertTrue('networks' in res.json)

    def test_create_network(self):
        data = {'network': {'name': 'net1', 'admin_state_up': True}}
        return_value = {'subnets': [], 'tags': []}
        return_value.update(data['network'].copy())

        instance = self.plugin.return_value
        instance.create_network.return_value = return_value

        res = self.api.post_json(_get_path('networks'), data)
        self.assertEqual(res.status_int, 201)

    def test_create_network_no_body(self):
        data = {'whoa': None}
        res = self.api.post_json(_get_path('networks'), data,
                                 expect_errors=True)
        self.assertEqual(res.status_int, 400)

    def test_create_network_no_resource(self):
        res = self.api.post_json(_get_path('networks'), dict(),
                                 expect_errors=True)
        self.assertEqual(res.status_int, 400)

    def test_create_network_missing_attr(self):
        data = {'network': {'what': 'who'}}
        res = self.api.post_json(_get_path('networks'), data,
                                 expect_errors=True)
        self.assertEqual(res.status_int, 422)

    def test_create_network_bulk(self):
        data = {'networks': [{'name': 'net1', 'admin_state_up': True},
                             {'name': 'net2', 'admin_state_up': True}]}

        def side_effect(context, network):
            nets = network.copy()
            for net in nets['networks']:
                net.update({'subnets': [], 'tags': []})
            return nets

        instance = self.plugin.return_value
        instance.create_network.side_effect = side_effect

        res = self.api.post_json(_get_path('networks'), data)
        self.assertEqual(res.status_int, 201)

    def test_create_network_bulk_no_networks(self):
        data = {'networks': []}
        res = self.api.post_json(_get_path('networks'), data,
                                 expect_errors=True)
        self.assertEqual(res.status_int, 400)

    def test_create_network_bulk_missing_attr(self):
        data = {'networks': [{'what': 'who'}]}
        res = self.api.post_json(_get_path('networks'), data,
                                 expect_errors=True)
        self.assertEqual(res.status_int, 422)

    def test_create_network_bulk_partial_body(self):
        data = {'networks': [{'name': 'net1', 'admin_state_up': True},
                             {}]}
        res = self.api.post_json(_get_path('networks'), data,
                                 expect_errors=True)
        self.assertEqual(res.status_int, 422)
