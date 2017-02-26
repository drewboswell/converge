# -*- coding: utf-8 -*-

from .LoadDataFromDisk import LoadDataFromDisk
import yaml
import os
import re
import logging


class LoadHierarchy(LoadDataFromDisk):

    @staticmethod
    def get_regex_hierarchy(hierarchy):
        regex_hierarchy = []
        for hiera in hierarchy:
            regex_hiera = dict()
            regex_hiera['hiera'] = hiera
            regex_hiera['regex'] = os.path.join(re.sub("\${.+?}", "([^/]+)", hiera))
            regex_hiera['tags'] = re.findall("\$\{([^/]+)\}", hiera)
            regex_hiera['glob'] = os.path.join(re.sub("\${.+?}", "*", hiera))
            regex_hierarchy.append(regex_hiera)
        return regex_hierarchy

    def merge_contents_of_files(self, file_list):
        contents = list()
        all_yaml_individual = map(lambda x: yaml.load_all(open(x)), file_list)
        for configs in all_yaml_individual:
            for config in configs:
                contents.extend(config)
        return contents

    def load_contents_of_files(self, glob_pattern=None):
        file_list = self.get_list_of_files(glob_pattern=glob_pattern, recursive=False)
        content = self.merge_contents_of_files(file_list=file_list)
        return content

    def run(self, data, conf, **kwargs):
        base_dir = conf["programs"]["host"]["conf"]["hierarchy"]["base_dir"]
        property_mapping_glob = conf["programs"]["host"]["conf"]["hierarchy"]["hierarchy_glob"]
        glob_pattern = os.path.join(base_dir, property_mapping_glob)
        data.data["hierarchy"] = self.get_regex_hierarchy(self.load_contents_of_files(glob_pattern=glob_pattern))
        return data
