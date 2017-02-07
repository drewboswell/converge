# -*- coding: utf-8 -*-

from .LoadDataFromDisk import LoadDataFromDisk
import yaml
import os
import logging


class LoadHierarchy(LoadDataFromDisk):
    def merge_contents_of_files(self, file_list):
        contents = list()
        all_yaml_individual = map(lambda x: yaml.load_all(open(x)), file_list)
        for configs in all_yaml_individual:
            for config in configs:
                contents.extend(config)
        return contents

    def load_contents_of_files(self, base_directory="."):
        glob_pattern = os.path.join(base_directory, "hierarchy.yaml")
        file_list = self.get_list_of_files(glob_pattern=glob_pattern, recursive=False)
        content = self.merge_contents_of_files(file_list=file_list)
        return content


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
        data.targets = self.load_contents_of_files(glob_pattern=glob_pattern)
        return data


class FilterHostsByHost:
    @staticmethod
    def run(data, conf, **kwargs):
        host_filter = kwargs.get("host_name")
        filtered_targets = dict()
        if host_filter in data.targets:
            filtered_targets[host_filter] = data.targets[host_filter]
        data.targets = filtered_targets
        return data


class FilterHostsByTag:
    @staticmethod
    def run(data, conf, **kwargs):
        tag_name = kwargs.get("tag_name")
        tag_value = kwargs.get("tag_value")
        filtered_targets = dict()
        for host_name, host_tags in data.targets.items():
            if tag_name in host_tags and host_tags[tag_name] == tag_value:
                filtered_targets[host_name] = host_tags
        data.targets = filtered_targets
        return data


class PrintTagsForHost:
    @staticmethod
    def run(data, conf, **kwargs):
        for host_name, host_tags in data.targets.items():
            message = "HOST TAG LOOKUP \n %s tags:\n\t%s"
            logging.info(message % (host_name, str(host_tags)))
        return data


class PrintHostsForTag:
    @staticmethod
    def run(data, conf, **kwargs):
        message = "TAG TO HOST LOOKUP \n TAG: %s=%s has hosts:\n\t%s"
        tag_name = kwargs.get("tag_name")
        tag_value = kwargs.get("tag_value")
        logging.info(message % (tag_name, tag_value, list(data.targets.keys())))
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
