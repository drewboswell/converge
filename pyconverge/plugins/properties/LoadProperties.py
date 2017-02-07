# -*- coding: utf-8 -*-

from .LoadDataFromDisk import LoadDataFromDisk
import configparser
from itertools import chain
import logging
import re
import os


class LoadProperties(LoadDataFromDisk):
    def __init__(self, hierarchy, host_tags, repository_path):
        self.host_tags = host_tags
        self.hierarchy = hierarchy
        self.repository_path = repository_path
        self.regex_hierarchy = self.get_regex_hierarchy(hierarchy=hierarchy)

    def merge_contents_of_files(self, file_list):
        parser = configparser.ConfigParser(allow_no_value=True)
        for file_path in file_list:
            with open(file_path) as lines:
                lines = chain(("[default]",), lines)  # This line does the trick...
                parser.read_file(lines)

        contents = parser.items("default")
        return contents

    def load_contents_of_files(self):
        pass

    def get_regex_hierarchy(self, hierarchy):
        regex_hierarchy = []
        for hiera in hierarchy:
            regex_hiera = dict()
            regex_hiera['hiera'] = hiera
            regex_hiera['regex'] = os.path.join(self.repository_path, re.sub("\${.+?}", "([^/]+)", hiera))
            regex_hiera['tags'] = re.findall("\$\{([^/]+)\}", hiera)
            regex_hierarchy.append(regex_hiera)
        return regex_hierarchy

    def filter_hierarchy(self, file_list):
        filtered_hierarchy = list()
        for file_path in file_list:
            for hiera in self.regex_hierarchy:
                if re.match(hiera['regex'], os.path.dirname(file_path)):
                    filtered_hierarchy.append(hiera)
        return filtered_hierarchy

    def filter_file_list_by_host_tags(self, file_list, filtered_hierarchy, application_name):
        content = list()
        for file_path in file_list:
            for hiera in filtered_hierarchy:
                regex = re.findall(hiera["regex"], os.path.dirname(file_path))
                if regex:
                    result = True
                    for i, tag in enumerate(regex):
                        if not hiera['tags'] and tag.rsplit("/", 1)[1] == "default":
                            break
                        elif hiera['tags'][i] == "app":
                            if application_name != tag:
                                result = False
                                break
                        elif hiera['tags'][i] in self.host_tags:
                            break
                        else:
                            result = False
                            break
                    if result:
                        content.append(file_path)
        return content

    def get_file_list_ordered_by_hierarchy(self, file_list, application_name, application_tags):
        content = list()
        hierarchy = self.filter_hierarchy(file_list)
        filtered_file_list = self.filter_file_list_by_host_tags(file_list=file_list,
                                                                filtered_hierarchy=hierarchy,
                                                                application_name=application_name)
        if len(filtered_file_list) > 0:
            for hiera in hierarchy:
                for file_path in filtered_file_list:
                    if re.match(hiera['regex'], file_path):
                        content.append(file_path)
                        filtered_file_list.remove(file_path)
        return content

    def load_contents_of_property_by_pattern(self, file_name, application_name, application_tags):
        content = list()
        logging.info("Loading Contents for %s" % application_name)
        glob_pattern = os.path.join(self.repository_path, "**", file_name + ".properties")
        file_list = self.get_list_of_files(glob_pattern=glob_pattern, recursive=True)
        file_list_order_by_hierarchy = self.get_file_list_ordered_by_hierarchy(file_list=file_list,
                                                                               application_name=application_name,
                                                                               application_tags=application_tags)
        if file_list_order_by_hierarchy:
            content = self.merge_contents_of_files(file_list=file_list_order_by_hierarchy)
        return content

    def load_contents_of_property_list(self, application_name, application_tags):
        content = dict()
        import time
        start = time.time()
        for file_path in application_tags['properties']:
            result = self.load_contents_of_property_by_pattern(file_name=file_path,
                                                               application_name=application_name,
                                                               application_tags=application_tags)
            if result:
                content[file_path] = result
        logging.info("TIMING load_contents_of_property_list %s %f" % (application_name, time.time() - start))
        return content
