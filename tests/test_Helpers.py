# -*- coding: utf-8 -*-

import pytest
import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join('..', 'converge')))
from converge.Helpers import Helpers as Helpers


class TestHelpers(unittest.TestCase):

    def setUp(self):
        self.helpers = Helpers()

    def test_get_directory_tree_exists(self):
        result = False
        directory_path = "converge/resources"
        returned = self.helpers.get_directory_tree(directory_path=directory_path)
        print(returned)
        if isinstance(returned, list) and returned is not None and len(returned) > 1:
            result = True
        self.assertTrue(result)

    def test_get_directory_tree_not_exists(self):
        result = False
        directory_path = "converge/resources_not_exists"
        returned = self.helpers.get_directory_tree(directory_path=directory_path)
        print(returned)
        if isinstance(returned, list) and returned == []:
            result = False
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()