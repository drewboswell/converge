# -*- coding: utf-8 -*-
import re

def find_dict_diff(d1, d2, path=""):
    result = False
    for k in d1.keys():
        if k not in d2:
            continue
        elif isinstance(d1[k], dict):
            if path == "":
                path = k
            else:
                path = path + "->" + k
            result = find_dict_diff(d1[k], d2[k], path)
        elif d1[k] == d2[k] or \
                (isinstance(d1[k], list)
                 and isinstance(d2[k], list)
                 and len(set(d1[k]).intersection(set(d2[k]))) > 0):
            return True
    return result


class FilterHostsByHost:
    @staticmethod
    def run(data, conf, **kwargs):
        data_filter = kwargs.get("host_name")
        filtered_targets = list()
        if data_filter in data.targets["hosts"]:
            filtered_targets.append(data_filter)
        data.targets["hosts"] = filtered_targets
        return data


class FilterHostsByTag:
    @staticmethod
    def run(data, **kwargs):
        tag_name = kwargs.get("tag_name")
        tag_value = kwargs.get("tag_value")
        filtered_targets = list()
        for host_name in data.targets["hosts"]:
            host_tags = data.data["hosts"][host_name]
            if tag_name in host_tags and (
                        (isinstance(host_tags[tag_name], str) and host_tags[tag_name] == tag_value) or
                        (isinstance(host_tags[tag_name], list) and any(
                                host_value == tag_value for host_value in host_tags[tag_name]))):
                filtered_targets.append(host_name)
        data.targets["hosts"] = filtered_targets
        return data


class FilterHostsByApplication:
    @staticmethod
    def run(data, **kwargs):
        application_name = kwargs.get("application_name")
        filtered_data = list()
        if application_name in data.targets["applications"]:
            application_tags = data.data["application_hosts"][application_name]
            for host_name in data.targets["hosts"]:
                host_tags = data.data["hosts"][host_name]
                host_app_tag_match = find_dict_diff(host_tags, application_tags)
                if host_app_tag_match:
                    filtered_data.append(host_name)
        data.targets["hosts"] = filtered_data
        return data


class FilterApplicationsByTag:
    @staticmethod
    def run(data, **kwargs):
        tag_name = kwargs.get("tag_name")
        tag_value = kwargs.get("tag_value")
        filtered_targets = list()
        for application_name in data.targets["applications"]:
            application_tags = data.data["application_hosts"][application_name]
            if tag_name in application_tags and (
                        (isinstance(application_tags[tag_name], str)
                         and application_tags[tag_name] == tag_value) or
                        (isinstance(application_tags[tag_name], list)
                         and any(app_value == tag_value for app_value in application_tags[tag_name]))):
                filtered_targets.append(application_name)
        data.targets["applications"] = filtered_targets
        return data


class FilterApplicationsByHost:
    @staticmethod
    def run(data, **kwargs):
        host_name = kwargs.get("host_name")
        filtered_data = list()
        if host_name in data.data["hosts"]:
            host_tags = data.data["hosts"][host_name]
            for application_name in data.targets["applications"]:
                application_tags = data.data["application_hosts"][application_name]
                app_host_tag_match = find_dict_diff(application_tags, host_tags)
                if app_host_tag_match:
                    filtered_data.append(application_name)
        data.targets["applications"] = filtered_data
        return data


class FilterApplicationsByApplication:
    @staticmethod
    def run(data, **kwargs):
        data_filter = kwargs.get("application_name")
        filtered_targets = list()
        if data_filter in data.targets["applications"]:
            filtered_targets.append(data_filter)
        data.targets["applications"] = filtered_targets
        return data


class FilterApplicationsByProperty:
    @staticmethod
    def run(data, **kwargs):
        property_name = kwargs.get("property_name")
        filtered_targets = list()
        for application_name in data.targets["applications"]:
            application_props = data.data["application_properties"][application_name]
            if "properties" in application_props and \
                    isinstance(application_props["properties"], list) and \
                            property_name in application_props["properties"]:
                filtered_targets.append(application_name)
        data.targets["applications"] = filtered_targets
        return data


class FilterHierarchyByHost:
    @staticmethod
    def run(data, **kwargs):
        host_name = kwargs.get("host_name")
        filtered_data = list()
        if host_name in data.data["hosts"]:
            host_tags = data.data["hosts"][host_name].keys()
            for hiera in data.data["hierarchy"]:
                hiera_tags = hiera["tags"]
                if all(hiera_tag in host_tags or hiera_tag == "app" for hiera_tag in hiera_tags):
                    filtered_data.append(hiera)
        data.data["hierarchy"] = filtered_data
        return data


class FilterPropertyFilesByApplication:
    @staticmethod
    def run(data, **kwargs):
        application_name = kwargs.get("application_name")
        filtered_data = data.data["file_hiera"].copy()
        if application_name in data.data["application_properties"]:
            property_files = data.data["application_properties"][application_name]
            for hiera_file in data.data["file_hiera"].keys():
                if hiera_file not in property_files["properties"]:
                    del filtered_data[hiera_file]
        data.data["file_hiera"] = filtered_data
        return data


class FilterPropertyFilesByHostApplicationTags:
    @staticmethod
    def run(data, **kwargs):
        host_name = kwargs.get("host_name")
        application_name = kwargs.get("application_name")
        filtered_data = data.data["file_hiera"].copy()
        if host_name in data.data["hosts"]:
            host_tags = data.data["hosts"][host_name]
            # for each file in list of properties
            # check that path matches
            for file_name, file_datas in data.data["file_hiera"].items():
                for file_data in file_datas:
                    for hiera in data.data["hierarchy"]:
                        if file_data["hiera"] == hiera["hiera"] and len(hiera["tags"]) == len(file_data["tags"]):
                            for i, tag in enumerate(hiera["tags"]):
                                if (tag == "app" and file_data["tags"][i] != application_name) \
                                        or (tag in hiera["tags"] and file_data["tags"][i] in host_tags[tag]):
                                    filtered_data[file_name].remove(file_data)
        data.data["file_hiera"] = filtered_data
        return data