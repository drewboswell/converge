# -*- coding: utf-8 -*-

from .LoadDataFromDisk import LoadDataFromDisk
import yaml
import os
import glob
import re
import configparser
from itertools import chain
import logging


class LoadHosts(LoadDataFromDisk):
    def merge_contents_of_files(self, file_list):
        contents = dict()
        all_yaml_individual = map(lambda x: yaml.load_all(open(x)), file_list)
        for configs in all_yaml_individual:
            for config in configs:
                contents = {**contents, **config}
        return contents

    def load_contents_of_files(self, glob_pattern=None):
        file_list = self.get_list_of_files(glob_pattern=glob_pattern, recursive=False)
        content = self.merge_contents_of_files(file_list=file_list)
        return content

    def run(self, data, conf, **kwargs):
        base_dir = conf["programs"]["host"]["conf"]["properties"]["base_dir"]
        host_glob = conf["programs"]["host"]["conf"]["properties"]["host_glob"]
        glob_pattern = os.path.join(base_dir, host_glob)
        data.data["hosts"] = self.load_contents_of_files(glob_pattern=glob_pattern)
        data.targets["hosts"] = list(data.data["hosts"].keys())
        return data


class LoadApplicationHostMapping(LoadDataFromDisk):
    def merge_contents_of_files(self, file_list):
        contents = dict()
        for file_path in file_list:
            app_name = file_path.rsplit("/", 1)[1][:-5]
            for config in yaml.load_all(open(file_path)):
                contents[app_name] = config
        return contents

    def load_contents_of_files(self, glob_pattern=None):
        file_list = self.get_list_of_files(glob_pattern=glob_pattern, recursive=False)
        content = self.merge_contents_of_files(file_list=file_list)
        return content

    def run(self, data, conf, **kwargs):
        base_dir = conf["programs"]["host"]["conf"]["properties"]["base_dir"]
        host_mapping_glob = conf["programs"]["host"]["conf"]["properties"]["host_mapping_glob"]
        glob_pattern = os.path.join(base_dir, host_mapping_glob)
        data.data["application_hosts"] = self.load_contents_of_files(glob_pattern=glob_pattern)
        data.targets["applications"] = set(data.data["application_hosts"].keys())
        return data


class LoadApplicationPropertiesMapping(LoadDataFromDisk):
    def merge_contents_of_files(self, file_list):
        contents = dict()
        for file_path in file_list:
            app_name = file_path.rsplit("/", 3)[1]
            for config in yaml.load_all(open(file_path)):
                contents[app_name] = config
        return contents

    def load_contents_of_files(self, glob_pattern=None):
        file_list = self.get_list_of_files(glob_pattern=glob_pattern, recursive=False)
        content = self.merge_contents_of_files(file_list=file_list)
        return content

    def run(self, data, conf, **kwargs):
        base_dir = conf["programs"]["application"]["conf"]["properties"]["base_dir"]
        property_mapping_glob = conf["programs"]["application"]["conf"]["properties"]["property_mapping_glob"]
        glob_pattern = os.path.join(base_dir, property_mapping_glob)
        data.data["application_properties"] = self.load_contents_of_files(glob_pattern=glob_pattern)
        data.targets["applications"] = set(data.data["application_properties"].keys())
        return data


class LoadApplications(LoadDataFromDisk):
    def merge_contents_of_files(self, file_list):
        contents = dict()
        for file_path in file_list:
            app_name = file_path.rsplit("/", 1)[1][:-5]
            for config in yaml.load_all(open(file_path)):
                contents[app_name] = config
        return contents

    def load_contents_of_files(self, base_directory="."):
        glob_pattern = os.path.join(base_directory, "applications", "*.yaml")
        file_list = self.get_list_of_files(glob_pattern=glob_pattern, recursive=False)
        content = self.merge_contents_of_files(file_list=file_list)
        return content


class LoadPropertyFilePaths:

    def run(self, data, conf, **kwargs):
        base_dir = conf["programs"]["host"]["conf"]["properties"]["base_dir"]
        hierarchy = data.data["hierarchy"]
        file_list = dict()
        for hiera in hierarchy:
            hiera_path = hiera["glob"]
            for file_path in glob.iglob(os.path.join(base_dir, "data", hiera_path, '*.properties'), recursive=False):
                file_name = file_path.rsplit("/", 1)[1][:-11]
                if file_name not in file_list:
                    file_list[file_name] = list()
                if "${" in hiera["hiera"]:
                    tags = re.findall(hiera["regex"], file_path)
                else:
                    tags = []
                file_list[file_name].append({"hiera": hiera["hiera"],
                                             "path": file_path,
                                             "tags": tags})

        data.data["file_hiera"] = file_list
        return data


class LoadPropertyFileContents:

    def run(self, data, conf, **kwargs):
        file_list = data.data["file_hiera"]
        resolved_data = dict()
        for file_name, file_path_list in file_list.items():
            parser = configparser.ConfigParser(allow_no_value=True)
            for file_path in file_path_list:
                with open(file_path["path"]) as lines:
                    lines = chain(("[default]",), lines)  # This line does the trick...
                    parser.read_file(lines)

            contents = parser.items("default")
            resolved_data[file_name] = contents
        data.data["file_data"] = resolved_data
        return data