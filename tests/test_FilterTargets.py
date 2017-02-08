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
        self.data.targets = {
            "hosts": ["pre-host1", "pre-host2", "staging-host1", "staging-host2", "prod-host1", "prod-host2"],
            "applications": ["application1", "application2", "application3", "application4"]
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
        print(returns.targets)
        if isinstance(returns, object) \
                and isinstance(returns.targets["hosts"], list) \
                and len(returns.targets["hosts"]) == 1\
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
        print(returns.targets)
        if isinstance(returns, object) \
                and isinstance(returns.targets["hosts"], list) \
                and len(returns.targets["hosts"]) == 0:
            result = True
        self.assertTrue(result)

