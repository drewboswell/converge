# -*- coding: utf-8 -*-

from pykwalify.core import Core
import pykwalify
import glob
import yaml
import sys
import os
import time
import logging


class RepositoryReader:
    """
    this class holds the basic file manipulation, resolving and miscellaneous functions used by converge
    """

    def __init__(self, repository_path, node_path, node_group_path, package_path, package_group_path, hierarchy_path,
                 package_inheritance_depth_max, logging=logging):
        self.repository_path = repository_path
        self.node_path = node_path
        self.node_group_path = node_group_path
        self.package_path = package_path
        self.package_group_path = package_group_path
        self.hierarchy_path = hierarchy_path
        self.package_inheritance_depth_max = package_inheritance_depth_max

        self.root_dir = os.path.dirname(os.path.abspath(__file__))

        self.logging = logging
        self.logging.getLogger("pykwalify").setLevel(logging.WARNING)
        self.statistics = {}

        self.non_resolved_configuration = self.load_non_resolved_configuration()

        self.nodes = dict()
        self.node_groups = dict()
        self.packages = dict()
        self.applications = dict()
        self.hierarchy = dict()
        # self.node_applications allows connection between nodes -> application, also limits useless host lookups
        # (avoids full iteration where not necessary)
        self.node_applications = dict()

    def load_yaml_files_in_directory(self, directory):
        time_marker = time.time()
        result = dict()
        self.logging.info("Loading YAML Folder: %s" % directory)
        for filename_path in glob.iglob(os.path.join(directory, "*.yaml"), recursive=False):
            with open(filename_path, 'r') as f:
                filename_exploded = filename_path.split("/")
                filename = filename_exploded[-1][:-5]
                result[filename] = yaml.load(f)
                self.logging.info("Loaded YAML file: %s.yaml" % filename)

        self.statistics['load_yaml_files_%s' % directory.split("/")[-1]] = time.time() - time_marker
        return result

    def load_non_resolved_configuration(self):
        time_marker = time.time()
        non_resolved_configuration = dict()
        non_resolved_configuration['nodes'] = self.load_yaml_files_in_directory(directory=self.node_path)
        non_resolved_configuration['node_groups'] = self.load_yaml_files_in_directory(directory=self.node_group_path)
        non_resolved_configuration['packages'] = self.load_yaml_files_in_directory(directory=self.package_path)
        non_resolved_configuration['package_groups'] = self.load_yaml_files_in_directory(
            directory=self.package_group_path)
        non_resolved_configuration['hierarchy'] = self.load_yaml_files_in_directory(directory=self.hierarchy_path)
        self.statistics['load_yaml_all'] = time.time() - time_marker
        return non_resolved_configuration

    def validate_yaml_schema(self, target_path, schema_path):
        result = True
        self.logging.info("SCANNING: %s/**.yaml" % target_path)
        for filename_path in glob.iglob(os.path.join(target_path, "*.yaml"), recursive=False):
            self.logging.debug("Validating: %s" % filename_path)
            c = Core(source_file=filename_path, schema_files=[schema_path])
            try:
                c.validate(raise_exception=True)
            except pykwalify.errors.SchemaError:
                result = False
                pass
        if result:
            self.logging.info("VALIDATED: %s/**.yaml" % target_path)
        else:
            self.logging.error("Corrupt files!")
        return result

    def validate_node_yaml(self):
        target_path = self.node_path
        schema_path = os.path.join(self.root_dir, "schemas", "node_schema.yaml")
        result = self.validate_yaml_schema(target_path=target_path, schema_path=schema_path)
        return result

    def validate_node_group_yaml(self):
        target_path = self.node_group_path
        schema_path = os.path.join(self.root_dir, "schemas", "node_group_schema.yaml")
        result = self.validate_yaml_schema(target_path=target_path, schema_path=schema_path)
        return result

    def validate_package_yaml(self):
        target_path = self.package_path
        schema_path = os.path.join(self.root_dir, "schemas", "package_schema.yaml")
        result = self.validate_yaml_schema(target_path=target_path, schema_path=schema_path)
        return result

    def validate_package_group_yaml(self):
        target_path = self.package_group_path
        schema_path = os.path.join(self.root_dir, "schemas", "package_group_schema.yaml")
        result = self.validate_yaml_schema(target_path=target_path, schema_path=schema_path)
        return result

    def validate_hierarchy_yaml(self):
        target_path = self.hierarchy_path
        schema_path = os.path.join(self.root_dir, "schemas", "hierarchy_schema.yaml")
        result = self.validate_yaml_schema(target_path=target_path, schema_path=schema_path)
        return result
