# -*- coding: utf-8 -*-

import os
from shutil import copyfile, copytree
import pkg_resources
from .__init__ import __version__, __source_repository__, __release_repository__
from pyconverge.Helpers import Helpers
from pyconverge.RepositoryReader import RepositoryReader
import configparser
import logging
from pprint import pprint


class ConvergeOptions:

    def __init__(self):
        self.helpers = Helpers()
        self.logging = logging

        self.bin_dir = str()
        self.root_dir = str()
        self.conf_dir = str()
        self.config_path = str()
        self.repository_path = str()
        self.node_group_path = str()
        self.node_path = str()
        self.package_group_path = str()
        self.package_path = str()
        self.hierarchy_path = str()
        self.package_inheritance_depth_max = int()
        self.logging_level = str()
        self.reader = None

    @staticmethod
    def get_version_information():
        version_information = """
            Application Converge
            Version: {version_number:s}
            Project Source: {source_repository:s}
            Release repository: {release_repository:s}
            """
        version_arguments = {
            "version_number": __version__,
            "source_repository": __source_repository__,
            "release_repository": __release_repository__
        }
        return version_information.format(**version_arguments)

    @staticmethod
    def init_conf(target_directory):
        result = False
        init_path = os.path.isdir(os.path.join(target_directory,"converge.ini.template"))
        if not init_path:
            print("will create configuration file in %s/converge.ini.template" % target_directory)
            resource_package = __name__
            resource_path = os.path.join('resources', 'etc')
            template = pkg_resources.resource_filename(resource_package, resource_path)
            print("Copying template from %s to %s" % (template, target_directory))
            copytree(template, target_directory)
            print("New configuration can be found in: %s" % target_directory)
            result = os.path.isfile(os.path.join(target_directory, "converge.ini.template"))
        else:
            print("File already exists: %s/converge.ini.template" % target_directory)
        return result

    def init_repository(self, target_directory):
        result = False
        init_path = os.path.isdir(target_directory)
        if not init_path:
            print("will copy repository template into %s" % target_directory)
            resource_package = __name__
            resource_path = os.path.join('resources', 'repository')
            template = pkg_resources.resource_filename(resource_package, resource_path)
            print("Copying contents of repository template from %s to %s" % (template, target_directory))
            copytree(template, target_directory)
            print("Newly initialized repository can be found in: %s" % target_directory)
            dir_tree = self.helpers.get_directory_tree(target_directory)
            if isinstance(dir_tree, list) and len(dir_tree) > 0:
                result = True
        else:
            print("Folder already exists: %s" % target_directory)
        return result

    def check_config(self, config_path):
        result = False
        path_exists = os.path.isfile(config_path)
        if path_exists:
            print("Checking configuration at location: '%s'" % config_path)
            result = self.load_configuration(config_path=config_path)
            if result:
                print("\t## Configuration to be used:\n")
                print("\tRepository Path: '%s'" % self.repository_path)
                print("\tNode Path: '%s'" % self.node_path)
                print("\tNode Group Path: '%s'" % self.node_group_path)
                print("\tPackage Path: '%s'" % self.package_path)
                print("\tPackage Group Path: '%s'" % self.package_group_path)
                print("\tLogging Level: '%s'" % self.logging_level)
                print("\tMax Inheritance Depth: '%s'" % self.package_inheritance_depth_max)
                print("")
        else:
            print("File %s does not exist" % config_path)

        return result

    def load_configuration(self, config_path):
        result = True

        # Figure out where we're installed and set defaults
        self.bin_dir = os.path.dirname(os.path.abspath(__file__))
        self.root_dir = os.path.dirname(self.bin_dir)
        self.conf_dir = os.path.join(self.root_dir, 'etc')
        self.config_path = os.path.join(self.conf_dir, "converge.ini")

        config = configparser.ConfigParser()
        config.read(config_path)

        # set path for nodes
        if "logging_level" in config['DEFAULT']:
            self.logging_level = config["DEFAULT"]["logging_level"]
        else:
            self.logging_level = "INFO"

        self.logging.basicConfig(level=self.logging_level)

        # set path for repository
        if "repository_path" in config['DEFAULT']:
            self.repository_path = config["DEFAULT"]["repository_path"]
        else:
            self.repository_path = os.path.join(self.root_dir, "repository")

        # set path for nodes
        if "node_path" in config['DEFAULT']:
            self.node_path = config["DEFAULT"]["node_path"]
        else:
            self.node_path = os.path.join(self.repository_path, "nodes")

        # set path for node_groups
        if "node_group_path" in config['DEFAULT']:
            self.node_group_path = config["DEFAULT"]["node_group_path"]
        else:
            self.node_group_path = os.path.join(self.repository_path, "node_groups")

        # set path for packages
        if "package_path" in config['DEFAULT']:
            self.package_path = config["DEFAULT"]["package_path"]
        else:
            self.package_path = os.path.join(self.repository_path, "packages")

        # set path for applications
        if "package_group_path" in config['DEFAULT']:
            self.package_group_path = config["DEFAULT"]["package_group_path"]
        else:
            self.package_group_path = os.path.join(self.repository_path, "package_groups")

        # set path for hierarchy
        if "hierarchy_path" in config['DEFAULT']:
            self.hierarchy_path = config["DEFAULT"]["hierarchy_path"]
        else:
            self.hierarchy_path = os.path.join(self.repository_path, "hierarchy")

        # set recursion depth on package resolution
        if "package_recursion_depth_max" in config['DEFAULT']:
            self.package_inheritance_depth_max = config["DEFAULT"]["package_recursion_depth_max"]
        else:
            self.package_inheritance_depth_max = 7

        config_paths = [self.node_path, self.node_group_path, self.package_path, self.package_group_path, self.repository_path]

        for config_path in config_paths:
            if not os.path.exists(config_path):
                print("ERROR Path: '%s' Does not exist" % config_path)
                result = False

        return result

    def check_repository(self):
        result = True

        self.reader = RepositoryReader(repository_path=self.repository_path,
                                       node_path=self.node_path,
                                       node_group_path=self.node_group_path,
                                       package_path=self.package_path,
                                       package_group_path=self.package_group_path,
                                       hierarchy_path=self.hierarchy_path,
                                       logging=self.logging,
                                       package_inheritance_depth_max=self.package_inheritance_depth_max)

        returns = self.reader.validate_node_yaml()
        if returns is not True:
            result = False

        returns = self.reader.validate_node_group_yaml()
        if returns is not True:
                result = False

        returns = self.reader.validate_package_yaml()
        if returns is not True:
                result = False

        returns = self.reader.validate_package_group_yaml()
        if returns is not True:
            result = False

        returns = self.reader.validate_hierarchy_yaml()
        if returns is not True:
            result = False

        return result
