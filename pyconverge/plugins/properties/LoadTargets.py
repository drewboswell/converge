# -*- coding: utf-8 -*-

from .LoadDataFromDisk import LoadDataFromDisk
import yaml
import os
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
