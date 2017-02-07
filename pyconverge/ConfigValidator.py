# -*- coding: utf-8 -*-

import os
from shutil import copyfile, copytree
import pkg_resources
from .__init__ import __version__, __source_repository__, __release_repository__
import configparser
import logging
from pykwalify.core import Core
import pykwalify
import glob
import yaml
import sys


class ConfigValidator:
    def __init__(self):
        self.logging = logging
        self.paths = dict()
        self.plugins = str()
        self.logging_level = str()
        self.reader = None
        self.configuration = dict()

        # Figure out where we're installed and set defaults
        self.paths['bin_dir'] = os.path.dirname(os.path.abspath(__file__))
        self.paths['root_dir'] = os.path.dirname(self.paths['bin_dir'])

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
        init_path = os.path.isdir(os.path.join(target_directory, "converge.ini.template"))
        if not init_path:
            print("will create configuration file in %s/converge.ini.template" % target_directory)
            resource_package = __name__
            resource_path = os.path.join('resources', 'etc')
            template = pkg_resources.resource_filename(resource_package, resource_path)
            print("Copying template from %s to %s" % (template, target_directory))
            copytree(template, target_directory)
            print("New configuration can be found in: %s" % target_directory)
            print("Make you modifications and rename it to converge.ini")
            result = os.path.isfile(os.path.join(target_directory, "converge.ini.template"))
        else:
            print("File already exists: %s/converge.ini.template" % target_directory)
        return result

    @staticmethod
    def get_directory_tree(directory_path):
        tree = []
        for dirname, dirnames, filenames in os.walk(directory_path):
            for subdirname in dirnames:
                tree.append(os.path.join(dirname, subdirname))
            for filename in filenames:
                tree.append(os.path.join(dirname, filename))
        return tree

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
            dir_tree = self.get_directory_tree(target_directory)
            if isinstance(dir_tree, list) and len(dir_tree) > 0:
                result = True
        else:
            print("Folder already exists: %s" % target_directory)
        return result

    def load_config(self,config_path):
        result = False
        path_exists = os.path.isfile(config_path)
        if path_exists:
            print("Checking configuration at location: '%s'" % config_path)
            converge_schema_path = os.path.join(self.paths["bin_dir"], "schemas", "converge_schema.yaml")
            if self.validate_yaml_schema(target_path=os.path.dirname(config_path), schema_path=converge_schema_path):
                with open(config_path, 'r') as stream:
                    try:
                        self.configuration = yaml.load(stream)
                        result = True
                    except yaml.YAMLError as exc:
                        print(exc)
        else:
            print("File %s does not exist" % config_path)
        return result

    def check_config(self, config_path):
        result = self.load_config(config_path=config_path)

        if result:
            print("\t## Configuration to be used:\n")
            print("\tLogging Level: '%s'" % self.configuration['default']['logging_level'])
            print("\tAvailable programs: %s" % ", ".join(self.configuration['programs'].keys()))
            for prog in self.configuration['programs']:
                print("\n\t# \"%s\" Program Comfiguration:" % prog)
                for conf, subconfs in self.configuration['programs'][prog]['conf'].items():
                    for name, sub in subconfs.items():
                        print("\t%s : %s : %s" % (conf, name, sub))
            print("")

        return result

    # def load_configuration(self, config_path):
    #     result = True
    #
    #     # Figure out where we're installed and set defaults
    #     self.paths['bin_dir'] = os.path.dirname(os.path.abspath(__file__))
    #     self.paths['root_dir'] = os.path.dirname(self.paths['bin_dir'])
    #
    #     config = configparser.ConfigParser()
    #     config.read(config_path)
    #
    #     # set path for nodes
    #     if "logging_level" in config['DEFAULT']:
    #         self.logging_level = config["DEFAULT"]["logging_level"]
    #     else:
    #         self.logging_level = "INFO"
    #
    #     self.logging.basicConfig(level=self.logging_level)
    #
    #     # set path for repository
    #     if "repository_path" in config['DEFAULT']:
    #         self.paths['repository'] = config["DEFAULT"]["repository_path"]
    #     else:
    #         self.paths['repository'] = os.path.join(self.paths['root_dir'], "repository")
    #
    #     # set path for hierarchy
    #     if "hierarchy_path" in config['DEFAULT']:
    #         self.paths['hierarchy'] = config["DEFAULT"]["hierarchy_path"]
    #     else:
    #         self.paths['hierarchy'] = os.path.join(self.paths['repository'], "hierarchy")
    #
    #     # set path for base data (non-resolved)
    #     if "data_path" in config['DEFAULT']:
    #         self.paths['data'] = config["DEFAULT"]["data_path"]
    #     else:
    #         self.paths['data'] = os.path.join(self.paths['repository'], "data")
    #
    #     # set path for output path (where files are generated)
    #     if "output_path" in config['DEFAULT']:
    #         self.paths['output'] = config["DEFAULT"]["output_path"]
    #     else:
    #         self.paths['output'] = os.path.join(self.paths['repository'], "output")
    #
    #     # set path for targets (hosts/applications)
    #     if "target_path" in config['DEFAULT']:
    #         self.paths['target'] = config["DEFAULT"]["target_path"]
    #     else:
    #         self.paths['target'] = os.path.join(self.paths['repository'], "targets")
    #
    #     # set path for application targets
    #     if "application_path" in config['DEFAULT']:
    #         self.paths['application'] = config["DEFAULT"]["application_path"]
    #     else:
    #         self.paths['application'] = os.path.join(self.paths['target'], "applications")
    #
    #     # set path for host targets
    #     if "host_path" in config['DEFAULT']:
    #         self.paths['host'] = config["DEFAULT"]["host_path"]
    #     else:
    #         self.paths['host'] = os.path.join(self.paths['target'], "hosts")
    #
    #     for config_name, config_path in self.paths.items():
    #         if not os.path.exists(config_path):
    #             print("ERROR Path: '%s' Does not exist for %s" % (config_path, config_name))
    #             result = False
    #
    #     # set plugins list
    #     if "plugins" in config['CLASSES']:
    #         self.paths['plugins'] = config["CLASSES"]["plugins"]
    #     else:
    #         self.paths['plugins'] = "pyconverge.plugins.properties.PropertiesPlugin.PropertiesPlugin"
    #
    #     return result

    def validate_hierarchy_yaml(self):
        target_path = self.paths['hierarchy']
        schema_path = os.path.join(self.paths['bin_dir'], "schemas", "hierarchy_schema.yaml")
        result = self.validate_yaml_schema(target_path=target_path, schema_path=schema_path)
        return result

    def validate_host_yaml(self):
        target_path = self.paths['host']
        schema_path = os.path.join(self.paths['bin_dir'], "schemas", "host_schema.yaml")
        result = self.validate_yaml_schema(target_path=target_path, schema_path=schema_path)
        return result

    def validate_application_yaml(self):
        target_path = self.paths['application']
        schema_path = os.path.join(self.paths['bin_dir'], "schemas", "application_schema.yaml")
        result = self.validate_yaml_schema(target_path=target_path, schema_path=schema_path)
        return result

    def validate_yaml_schema(self, target_path, schema_path):
        result = True
        self.logging.info("SCANNING: %s/**.yaml" % target_path)
        for filename_path in glob.iglob(os.path.join(target_path, "*.yaml")):
            self.logging.debug("Validating: %s" % filename_path)
            c = Core(source_file=filename_path, schema_files=[schema_path])
            try:
                c.validate(raise_exception=True)
            except pykwalify.errors.SchemaError:
                result = False
        if result:
            self.logging.info("VALIDATED: %s/**.yaml" % target_path)
        else:
            self.logging.error("Corrupt files!")
        return result

    def check_repository(self):
        result = True

        returns = self.validate_hierarchy_yaml()
        if returns is not True:
            result = False

        returns = self.validate_host_yaml()
        if returns is not True:
            result = False

        returns = self.validate_application_yaml()
        if returns is not True:
            result = False

        return result

    def get_configuration_paths(self):
        return self.paths
