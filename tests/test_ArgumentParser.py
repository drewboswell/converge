# -*- coding: utf-8 -*-

import pytest
import unittest
import sys
import os
import argparse
sys.path.append(os.path.abspath(os.path.join('..', 'converge')))
from pyconverge.ArgumentParser import ArgumentParser as ArgumentParser


class TestArgumentParser(unittest.TestCase):

    def setUp(self):
        self.argumentparser = ArgumentParser()

    def test_create_parser(self):
        result = False
        returns = self.argumentparser.create_parser()
        print(type(returns))
        if isinstance(returns, argparse.ArgumentParser):
            result = True
        self.assertTrue(result)

