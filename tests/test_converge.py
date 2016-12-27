# -*- coding: utf-8 -*-

import pytest
import argparse
import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join('..', 'converge')))
from pyconverge import converge as converge
import pyconverge.__main__ as mainexec


class TestConverge(unittest.TestCase):

    def test_main_arg_parser(self):
        try:
            result = converge.main()
        except argparse.ArgumentError:
            result = True
        self.assertTrue(result)

    def test_package_executable_main(self):
        try:
            result = mainexec.main()
        except argparse.ArgumentError:
            result = True
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
