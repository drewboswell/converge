# -*- coding: utf-8 -*-

import os
from shutil import copyfile, copytree
import pkg_resources
from .__init__ import __version__, __source_repository__, __release_repository__
from converge.Helpers import Helpers


class ConvergeOptions:

    def __init__(self):
        self.helpers = Helpers()

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

