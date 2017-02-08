# # -*- coding: utf-8 -*-
#
# import pytest
# import unittest
# import sys
# import os
#
# sys.path.append(os.path.abspath(os.path.join('..', 'converge')))
# from pyconverge.RepositoryReader import RepositoryReader
#
#
# class TestRepositoryReader(unittest.TestCase):
#     def setUp(self):
#         self.repository_path = "tests/resources/repository"
#         self.node_path = "tests/resources/repository/nodes"
#         self.node_group_path = "tests/resources/repository/node_groups"
#         self.package_path = "tests/resources/repository/packages"
#         self.package_group_path = "tests/resources/repository/package_groups"
#         self.hierarchy_path = "tests/resources/repository/hierarchy"
#         self.package_inheritance_depth_max = 7
#
#         args = {
#             "hierarchy_path": self.hierarchy_path,
#             "repository_path": self.repository_path,
#             "node_path": self.node_path,
#             "node_group_path": self.node_group_path,
#             "package_path": self.package_path,
#             "package_group_path": self.package_group_path,
#             "package_inheritance_depth_max": self.package_inheritance_depth_max
#         }
#         self.repositoryreader = RepositoryReader(**args)
#
#     def test_load_yaml_files_in_directory(self):
#         result = False
#         returns = self.repositoryreader.load_yaml_files_in_directory(self.hierarchy_path)
#         if isinstance(returns, dict) and 'nodes::nodes' in returns['hierarchy']['node::hierarchy']:
#             result = True
#         self.assertTrue(result)
#
#     def test_load_non_resolved_configuration(self):
#         result = False
#         returns = self.repositoryreader.load_non_resolved_configuration()
#         if isinstance(returns, dict) \
#                 and returns["hierarchy"] \
#                 and returns["nodes"] \
#                 and returns["node_groups"] \
#                 and returns["packages"] \
#                 and returns["package_groups"]:
#             result = True
#         self.assertTrue(result)
#
#     def test_validate_yaml_schema(self):
#         result = False
#         args = {
#             "target_path": self.hierarchy_path,
#             "schema_path": os.path.join("pyconverge", "schemas", "hierarchy_schema.yaml")
#         }
#         returns = self.repositoryreader.validate_yaml_schema(**args)
#         if returns is True:
#             result = True
#         self.assertTrue(result)
#
#     def test_validate_node_yaml(self):
#         result = False
#         returns = self.repositoryreader.validate_node_yaml()
#         if returns is True:
#             result = True
#         self.assertTrue(result)
#
#     def test_validate_node_group_yaml(self):
#         result = False
#         returns = self.repositoryreader.validate_node_group_yaml()
#         if returns is True:
#             result = True
#         self.assertTrue(result)
#
#     def test_validate_package_yaml(self):
#         result = False
#         returns = self.repositoryreader.validate_package_yaml()
#         if returns is True:
#             result = True
#         self.assertTrue(result)
#
#     def test_validate_package_group_yaml(self):
#         result = False
#         returns = self.repositoryreader.validate_package_group_yaml()
#         if returns is True:
#             result = True
#         self.assertTrue(result)
#
#     def test_validate_hierarchy_yaml(self):
#         result = False
#         returns = self.repositoryreader.validate_hierarchy_yaml()
#         if returns is True:
#             result = True
#         self.assertTrue(result)