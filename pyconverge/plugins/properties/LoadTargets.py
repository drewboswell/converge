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
        data.data_target_map["application_hosts"] = self.load_contents_of_files(glob_pattern=glob_pattern)
        data.targets["applications"] = set(data.data_target_map["application_hosts"].keys())
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
        data.data_group_data_map = self.load_contents_of_files(glob_pattern=glob_pattern)
        return data


class FilterApplicationsByApplication:
    @staticmethod
    def run(data, conf, **kwargs):
        data_filter = kwargs.get("application_name")
        filtered_targets = dict()
        if data_filter in data.data_target_map:
            filtered_targets[data_filter] = data.data_target_map[data_filter]
        data.data_target_map = filtered_targets
        return data


class FilterApplicationsByProperty:
    @staticmethod
    def run(data, conf, **kwargs):
        property_name = kwargs.get("property_name")
        filtered_targets = dict()
        for application_name, application_props in data.data_group_data_map.items():
            if "properties" in application_props and \
                    isinstance(application_props["properties"], list) and \
                            property_name in application_props["properties"]:
                filtered_targets[application_name] = application_props
        data.data_group_data_map = filtered_targets
        return data


class PrintTagsForHost:
    @staticmethod
    def run(data, conf, **kwargs):
        for host_name, host_tags in data.targets.items():
            message = "HOST TAG LOOKUP \n %s tags:\n\t%s"
            logging.info(message % (host_name, str(host_tags)))
        return data





class PrintTagsForApplication:
    @staticmethod
    def run(data, conf, **kwargs):
        message = "APPLICATION TO TAG LOOKUP \n APPLICATION: %s has tags:\n\t%s"
        application_name = kwargs.get("application_name")
        logging.info(message % (application_name, data.data_target_map[application_name]))
        return data


class PrintPropertiesForApplication:
    @staticmethod
    def run(data, conf, **kwargs):
        message = "APPLICATION TO PROPERTIES LOOKUP \n APPLICATION: %s has properties:\n\t%s"
        appliation_name = kwargs.get("application_name")
        logging.info(message % (appliation_name, list(data.data_group_data_map[appliation_name]["properties"])))
        return data


class PrintApplicationsForProperty:
    @staticmethod
    def run(data, conf, **kwargs):
        message = "PROPERTIES TO APPLICATION LOOKUP \n PROPERTIES: %s has applications:\n\t%s"
        property_name = kwargs.get("property_name")
        logging.info(message % (property_name, list(data.data_group_data_map.keys())))
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
