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


class LoadApplicationInfraMapping(LoadDataFromDisk):
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
        data.data_target_map = self.load_contents_of_files(glob_pattern=glob_pattern)
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


class FilterHostsByHost:
    @staticmethod
    def run(data, conf, **kwargs):
        data_filter = kwargs.get("host_name")
        filtered_targets = dict()
        if data_filter in data.targets:
            filtered_targets[data_filter] = data.targets[data_filter]
        data.targets = filtered_targets
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


class FilterApplicationsByTag:
    @staticmethod
    def run(data, conf, **kwargs):
        tag_name = kwargs.get("tag_name")
        tag_value = kwargs.get("tag_value")
        filtered_targets = dict()
        for application_name, application_tags in data.data_target_map.items():
            if tag_name in application_tags and (
                        (isinstance(application_tags[tag_name], str)
                         and application_tags[tag_name] == tag_value) or
                        (isinstance(application_tags[tag_name], list)
                         and any(app_value == tag_value for app_value in application_tags[tag_name]))):
                filtered_targets[application_name] = application_tags
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


class FilterApplicationsByHost:
    @staticmethod
    def run(data, conf, **kwargs):
        host_filter = kwargs.get("host_name")
        filtered_data = dict()
        if host_filter in data.targets:
            host_tags = data.targets[host_filter]
            for application_name, application_tags in data.data_target_map.items():
                for application_tag_name, application_tag_values in application_tags.items():
                    for host_tag_name, host_tag_values in host_tags.items():
                        if type(host_tag_name) == type(application_tag_name) and type(host_tag_values) == type(
                                application_tag_values):
                            if (isinstance(host_tag_values, str) and host_tag_values == application_tag_values or \
                                        (isinstance(host_tag_values, list) and set(host_tag_values).intersection(
                                            application_tag_values))):
                                filtered_data[application_name] = data.data_target_map[application_name]
        data.data_target_map = filtered_data
        return data


class FilterHostsByApplication:
    @staticmethod
    def run(data, conf, **kwargs):
        application_filter = kwargs.get("application_name")
        filtered_data = dict()
        if application_filter in data.data_target_map:
            application_tags = data.data_target_map[application_filter]
            for host_name, host_tags in data.targets.items():
                for host_tag_name, host_tag_values in host_tags.items():
                    for application_tag_name, application_tag_values in application_tags.items():
                        if type(host_tag_name) == type(application_tag_name) and type(host_tag_values) == type(
                                application_tag_values):
                            if (isinstance(host_tag_values, str) and host_tag_values == application_tag_values or \
                                        (isinstance(host_tag_values, list) and set(host_tag_values).intersection(
                                            application_tag_values))):
                                filtered_data[host_name] = data.targets[host_name]
        data.targets = filtered_data
        return data


class FilterHostsByTag:
    @staticmethod
    def run(data, conf, **kwargs):
        tag_name = kwargs.get("tag_name")
        tag_value = kwargs.get("tag_value")
        filtered_targets = dict()
        for host_name, host_tags in data.targets.items():
            if tag_name in host_tags and (
                        (isinstance(host_tags[tag_name], str) and host_tags[tag_name] == tag_value) or
                        (isinstance(host_tags[tag_name], list) and any(
                                host_value == tag_value for host_value in host_tags[tag_name]))):
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


class PrintApplicationsForHost:
    @staticmethod
    def run(data, conf, **kwargs):
        message = "HOST TO APPLICATION LOOKUP \n HOST: %s has applications:\n\t%s"
        host_name = kwargs.get("host_name")
        logging.info(message % (host_name, list(data.data_target_map.keys())))
        return data


class PrintHostsForApplication:
    @staticmethod
    def run(data, conf, **kwargs):
        message = "APPLICATION TO HOST LOOKUP \n APPLICATION: %s has hosts:\n\t%s"
        application_name = kwargs.get("application_name")
        logging.info(message % (application_name, list(data.targets.keys())))
        return data


class PrintHostsForTag:
    @staticmethod
    def run(data, conf, **kwargs):
        message = "TAG TO HOST LOOKUP \n TAG: %s=%s has hosts:\n\t%s"
        tag_name = kwargs.get("tag_name")
        tag_value = kwargs.get("tag_value")
        logging.info(message % (tag_name, tag_value, list(data.targets.keys())))
        return data


class PrintTagsForApplication:
    @staticmethod
    def run(data, conf, **kwargs):
        message = "APPLICATION TO TAG LOOKUP \n APPLICATION: %s has tags:\n\t%s"
        application_name = kwargs.get("application_name")
        logging.info(message % (application_name, data.data_target_map[application_name]))
        return data


class PrintApplicationsForTag:
    @staticmethod
    def run(data, conf, **kwargs):
        message = "TAG TO APPLICATION LOOKUP \n TAG: %s=%s has applications:\n\t%s"
        tag_name = kwargs.get("tag_name")
        tag_value = kwargs.get("tag_value")
        logging.info(message % (tag_name, tag_value, list(data.data_target_map.keys())))
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
