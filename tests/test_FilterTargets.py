# -*- coding: utf-8 -*-

import pytest
import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join('..', 'converge')))
from pyconverge.BaseClassLoader import ConvergeData
import pyconverge.plugins.properties.FilterTargets as FilterTargets


class TestFilterTargets(unittest.TestCase):
    def setUp(self):
        self.data = ConvergeData()
        self.data.data = {
            'hosts': {
                'pre-host2': {'datacenter': 'ONE', 'network': 'PRE', 'pool': ['hostgroup2'], 'environment': 'pre'},
                'staging-host1': {'datacenter': 'ONE', 'network': 'DMZ', 'pool': ['hostgroup1'],
                                  'environment': 'staging'},
                'prod-host10': {'datacenter': 'TWO', 'network': 'SEC', 'pool': ['hostgroup4'], 'environment': 'prod'},
                'prod-host2': {'datacenter': 'TWO', 'network': 'DMZ', 'pool': ['hostgroup1'], 'environment': 'prod'},
                'prod-host7': {'datacenter': 'ONE', 'network': 'DMZ', 'pool': ['hostgroup2'], 'environment': 'prod'},
                'pre-host1': {'datacenter': 'ONE', 'network': 'PRE', 'pool': ['hostgroup1'], 'environment': 'pre'},
                'uat-host2': {'datacenter': 'ONE', 'network': 'UAT', 'pool': ['hostgroup2'], 'environment': 'uat'},
                'dev-host3': {'datacenter': 'ONE', 'network': 'DEV', 'pool': ['hostgroup3'], 'environment': 'dev'},
                'prod-host1': {'datacenter': 'ONE', 'network': 'DMZ', 'pool': ['hostgroup1'], 'environment': 'prod'},
                'local-host1': {'datacenter': None, 'network': 'local', 'pool': ['hostgroup3'], 'environment': 'local'},
                'prod-host3': {'datacenter': 'ONE', 'network': 'DMZ', 'pool': ['hostgroup1'], 'environment': 'prod'},
                'prod-host11': {'datacenter': 'ONE', 'network': 'SEC', 'pool': ['hostgroup4'], 'environment': 'prod'},
                'uat-host4': {'datacenter': 'ONE', 'network': 'UAT', 'pool': ['hostgroup4'], 'environment': 'uat'},
                'staging-host3': {'datacenter': 'ONE', 'network': 'SEC', 'pool': ['hostgroup3'],
                                  'environment': 'staging'},
                'pre-host4': {'datacenter': 'ONE', 'network': 'PRE', 'pool': ['hostgroup4'], 'environment': 'pre'},
                'prod-host6': {'datacenter': 'TWO', 'network': 'DMZ', 'pool': ['hostgroup2'], 'environment': 'prod'},
                'dev-host1': {'datacenter': 'ONE', 'network': 'DEV', 'pool': ['hostgroup1'], 'environment': 'dev'},
                'staging-host4': {'datacenter': 'ONE', 'network': 'SEC', 'pool': ['hostgroup4'],
                                  'environment': 'staging'},
                'staging-host2': {'datacenter': 'ONE', 'network': 'DMZ', 'pool': ['hostgroup2'],
                                  'environment': 'staging'},
                'pre-host3': {'datacenter': 'ONE', 'network': 'PRE', 'pool': ['hostgroup3'], 'environment': 'pre'},
                'dev-host4': {'datacenter': 'ONE', 'network': 'DEV', 'pool': ['hostgroup4'], 'environment': 'dev'},
                'uat-host1': {'datacenter': 'ONE', 'network': 'UAT', 'pool': ['hostgroup1'], 'environment': 'uat'},
                'uat-host3': {'datacenter': 'ONE', 'network': 'UAT', 'pool': ['hostgroup3'], 'environment': 'uat'},
                'prod-host12': {'datacenter': 'TWO', 'network': 'SEC', 'pool': ['hostgroup4'], 'environment': 'prod'},
                'local-host2': {'datacenter': None, 'network': 'local', 'pool': ['hostgroup4'], 'environment': 'local'},
                'prod-host8': {'datacenter': 'TWO', 'network': 'DMZ', 'pool': ['hostgroup2'], 'environment': 'prod'},
                'prod-host5': {'datacenter': 'ONE', 'network': 'DMZ', 'pool': ['hostgroup2'], 'environment': 'prod'},
                'dev-host2': {'datacenter': 'ONE', 'network': 'DEV', 'pool': ['hostgroup2'], 'environment': 'dev'},
                'prod-host4': {'datacenter': 'TWO', 'network': 'DMZ', 'pool': ['hostgroup1'], 'environment': 'prod'},
                'prod-host9': {'datacenter': 'ONE', 'network': 'SEC', 'pool': ['hostgroup4'], 'environment': 'prod'}},
            'application_properties': {
                'application2': {'properties': ['propfile1']},
                'application3': {'properties': ['propfile1', 'propfile2', 'propfile3', 'propfile4']},
                'application1': {'properties': ['propfile1', 'propfile2']}
            },
            "application_hosts": {'application1': {'pool': ['hostgroup1', 'hostgroup2']},
                                  'application3': {'pool': ['hostgroup3', 'hostgroup2']},
                                  'application2': {'pool': ['hostgroup3', 'hostgroup4']}}
        }

        self.data.targets = {
            "hosts": ["pre-host1", "pre-host2", "staging-host1", "staging-host2", "prod-host1", "prod-host2"],
            "applications": ["application1", "application2", "application3"]
        }

    def test_FilterHostByHost_exists(self):
        result = False
        conf = dict
        host_name = "pre-host2"
        args = {"data": self.data,
                "conf": conf,
                "host_name": host_name}
        instance = FilterTargets.FilterHostsByHost()
        returns = instance.run(**args)
        if isinstance(returns, object) \
                and isinstance(returns.targets["hosts"], list) \
                and len(returns.targets["hosts"]) == 1 \
                and returns.targets["hosts"][0] == host_name:
            result = True
        self.assertTrue(result)

    def test_FilterHostByHost_not_exists(self):
        result = False
        conf = dict
        host_name = "pre-host5"
        args = {"data": self.data,
                "conf": conf,
                "host_name": host_name}
        instance = FilterTargets.FilterHostsByHost()
        returns = instance.run(**args)
        if isinstance(returns, object) \
                and isinstance(returns.targets["hosts"], list) \
                and len(returns.targets["hosts"]) == 0:
            result = True
        self.assertTrue(result)

    def test_FilterApplicationsByHost_exists(self):
        result = False
        conf = dict
        host_name = "pre-host1"
        args = {"data": self.data,
                "conf": conf,
                "host_name": host_name}
        instance = FilterTargets.FilterApplicationsByHost()
        returns = instance.run(**args)
        if isinstance(returns, object) \
                and isinstance(returns.targets["applications"], list) \
                and len(returns.targets["applications"]) == 1 \
                and returns.targets["applications"][0] == "application1":
            result = True
        self.assertTrue(result)

    def test_FilterApplicationsByHost_not_exists(self):
        result = False
        conf = dict
        host_name = "pre-host123"
        args = {"data": self.data,
                "conf": conf,
                "host_name": host_name}
        instance = FilterTargets.FilterApplicationsByHost()
        returns = instance.run(**args)
        if isinstance(returns, object) \
                and isinstance(returns.targets["applications"], list) \
                and len(returns.targets["applications"]) == 0:
            result = True
        self.assertTrue(result)

    def test_FilterHostsByTag_exists(self):
        result = False
        conf = dict
        tag_name = "pool"
        tag_value = "hostgroup1"
        expected = ['staging-host1', 'prod-host1', 'prod-host2', 'pre-host1']
        args = {"data": self.data,
                "conf": conf,
                "tag_name": tag_name,
                "tag_value": tag_value}
        instance = FilterTargets.FilterHostsByTag()
        returns = instance.run(**args)
        if isinstance(returns, object) \
                and isinstance(returns.targets["hosts"], list) \
                and len(returns.targets["hosts"]) > 0 \
                and set(returns.targets["hosts"]) == set(expected):
            result = True
        self.assertTrue(result)

    def test_FilterHostsByTag_not_exists(self):
        result = False
        conf = dict
        tag_name = "pool"
        tag_value = "hostgroup15"
        args = {"data": self.data,
                "conf": conf,
                "tag_name": tag_name,
                "tag_value": tag_value}
        instance = FilterTargets.FilterHostsByTag()
        returns = instance.run(**args)
        if isinstance(returns, object) \
                and isinstance(returns.targets["hosts"], list) \
                and len(returns.targets["hosts"]) == 0:
            result = True
        self.assertTrue(result)

    def test_FilterHostsByApplication_exists(self):
        result = False
        conf = dict
        application_name = "application1"
        expected = ['pre-host1', 'pre-host2', 'staging-host1', 'staging-host2', 'prod-host1', 'prod-host2']
        args = {"data": self.data,
                "conf": conf,
                "application_name": application_name}
        instance = FilterTargets.FilterHostsByApplication()
        returns = instance.run(**args)
        print(returns.targets["hosts"])
        if isinstance(returns, object) \
                and isinstance(returns.targets["hosts"], list) \
                and len(returns.targets["hosts"]) > 0 \
                and set(returns.targets["hosts"]) == set(expected):
            result = True
        self.assertTrue(result)

    def test_FilterHostsByApplication_not_exists(self):
        result = False
        conf = dict
        application_name = "application12"
        args = {"data": self.data,
                "conf": conf,
                "application_name": application_name}
        instance = FilterTargets.FilterHostsByApplication()
        returns = instance.run(**args)
        print(returns.targets["hosts"])
        if isinstance(returns, object) \
                and isinstance(returns.targets["hosts"], list) \
                and len(returns.targets["hosts"]) == 0:
            result = True
        self.assertTrue(result)

    def test_FilterApplicationsByTag_exists(self):
        result = False
        conf = dict
        tag_name = "pool"
        tag_value = "hostgroup2"
        expected = ['application1', 'application3']
        args = {"data": self.data,
                "conf": conf,
                "tag_name": tag_name,
                "tag_value": tag_value}
        instance = FilterTargets.FilterApplicationsByTag()
        returns = instance.run(**args)
        if isinstance(returns, object) \
                and isinstance(returns.targets["applications"], list) \
                and len(returns.targets["applications"]) > 0 \
                and set(returns.targets["applications"]) == set(expected):
            result = True
        self.assertTrue(result)

    def test_FilterApplicationsByTag_not_exists(self):
        result = False
        conf = dict
        tag_name = "pool"
        tag_value = "hostgroup24"
        args = {"data": self.data,
                "conf": conf,
                "tag_name": tag_name,
                "tag_value": tag_value}
        instance = FilterTargets.FilterApplicationsByTag()
        returns = instance.run(**args)
        if isinstance(returns, object) \
                and isinstance(returns.targets["applications"], list) \
                and len(returns.targets["applications"]) == 0:
            result = True
        self.assertTrue(result)

    def test_FilterApplicationsByApplication_exists(self):
        result = False
        conf = dict
        application_name = "application1"
        args = {"data": self.data,
                "conf": conf,
                "application_name": application_name}
        instance = FilterTargets.FilterApplicationsByApplication()
        returns = instance.run(**args)
        if isinstance(returns, object) \
                and isinstance(returns.targets["applications"], list) \
                and len(returns.targets["applications"]) == 1 \
                and returns.targets["applications"][0] == application_name:
            result = True
        self.assertTrue(result)

    def test_FilterApplicationsByApplication_not_exists(self):
        result = False
        conf = dict
        application_name = "application12"
        args = {"data": self.data,
                "conf": conf,
                "application_name": application_name}
        instance = FilterTargets.FilterApplicationsByApplication()
        returns = instance.run(**args)
        if isinstance(returns, object) \
                and isinstance(returns.targets["applications"], list) \
                and len(returns.targets["applications"]) == 0:
            result = True
        self.assertTrue(result)

    def test_FilterApplicationsByProperty_exists(self):
        result = False
        conf = dict
        expected = ['application1', 'application2', 'application3']
        property_name = "propfile1"
        args = {"data": self.data,
                "conf": conf,
                "property_name": property_name}
        instance = FilterTargets.FilterApplicationsByProperty()
        returns = instance.run(**args)
        print(returns.targets["applications"])
        if isinstance(returns, object) \
                and isinstance(returns.targets["applications"], list) \
                and len(returns.targets["applications"]) > 0 \
                and returns.targets["applications"] == expected:
            result = True
        self.assertTrue(result)

    def test_FilterApplicationsByProperty_not_exists(self):
        result = False
        conf = dict
        expected = ['application1', 'application2', 'application3']
        property_name = "propfile123"
        args = {"data": self.data,
                "conf": conf,
                "property_name": property_name}
        instance = FilterTargets.FilterApplicationsByProperty()
        returns = instance.run(**args)
        print(returns.targets["applications"])
        if isinstance(returns, object) \
                and isinstance(returns.targets["applications"], list) \
                and len(returns.targets["applications"]) == 0:
            result = True
        self.assertTrue(result)
