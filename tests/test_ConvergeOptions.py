# # -*- coding: utf-8 -*-
#
# import pytest
# import unittest
# import sys
# import os
# import shutil
# sys.path.append(os.path.abspath(os.path.join('..', 'converge')))
# from pyconverge.ConvergeOptions import ConvergeOptions
#
#
# class TestConvergeOptions(unittest.TestCase):
#
#     def setUp(self):
#         self.convergeoptions = ConvergeOptions()
#         self.convergeoptions.load_configuration(config_path="tests/resources/etc/converge.ini")
#
#     def test_opt_version(self):
#         result = False
#         returns = self.convergeoptions.get_version_information()
#         if isinstance(returns, str) and all(x in returns for x in ["Version","pypi","github"]):
#             result = True
#         self.assertTrue(result)
#
#     def test_opt_init_conf(self):
#         result = False
#         target_directory = os.path.join("tests","resources","generated_by_tests", "test_opt_init_conf")
#         returns = self.convergeoptions.init_conf(target_directory=target_directory)
#         if returns is True:
#             result = True
#         self.assertTrue(result)
#
#     def test_opt_init_repository(self):
#         result = False
#         target_directory = os.path.join("tests","resources","generated_by_tests", "test_opt_init_repository")
#         returns = self.convergeoptions.init_repository(target_directory=target_directory)
#         if returns is True:
#             result = True
#         self.assertTrue(result)
#
#     def test_check_config_exists(self):
#         result = False
#         target_directory = os.path.join("tests","resources","etc", "converge.ini")
#         returns = self.convergeoptions.check_config(config_path=target_directory)
#         if returns is True:
#             result = True
#         self.assertTrue(result)
#
#     def test_check_config_not_exist(self):
#         result = False
#         target_directory = os.path.join("tests","resources","etc", "converge.ini.shouldnt.exist")
#         returns = self.convergeoptions.check_config(config_path=target_directory)
#         if returns is False:
#             result = True
#         self.assertTrue(result)
#
#     def test_check_repository(self):
#         result = False
#         returns = self.convergeoptions.check_repository()
#         if returns is True:
#             result = True
#         self.assertTrue(result)
#
#     def tearDown(self):
#         temp_test_resources_path = os.path.join("tests","resources","generated_by_tests")
#         if os.path.isdir(os.path.join("tests","resources","generated_by_tests")):
#             shutil.rmtree(temp_test_resources_path)
