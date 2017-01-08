import glob
import os
import yaml
from abc import ABC, abstractmethod
import re
import configparser
from itertools import chain


class LoadDataFromDisk(ABC):
    @staticmethod
    def get_list_of_files(glob_pattern, recursive=False):
        return glob.glob(glob_pattern, recursive=recursive)

    @abstractmethod
    def merge_contents_of_files(self, file_list):
        pass

    @abstractmethod
    def load_contents_of_files(self):
        pass


class LoadHosts(LoadDataFromDisk):
    def merge_contents_of_files(self, file_list):
        contents = dict()
        all_yaml_individual = map(lambda x: yaml.load_all(open(x)), file_list)
        for configs in all_yaml_individual:
            for config in configs:
                contents = {**contents, **config}
        return contents

    def load_contents_of_files(self):
        glob_pattern = os.path.join("targets", "hosts", "*.yaml")
        file_list = self.get_list_of_files(glob_pattern=glob_pattern, recursive=False)
        content = self.merge_contents_of_files(file_list=file_list)
        return content


class LoadApplications(LoadDataFromDisk):
    def merge_contents_of_files(self, file_list):
        contents = dict()
        for file_path in file_list:
            app_name = file_path.rsplit("/", 1)[1][:-5]
            for config in yaml.load_all(open(file_path)):
                contents[app_name] = config
        return contents

    def load_contents_of_files(self):
        glob_pattern = os.path.join("targets", "applications", "*.yaml")
        file_list = self.get_list_of_files(glob_pattern=glob_pattern, recursive=False)
        content = self.merge_contents_of_files(file_list=file_list)
        return content


class LoadHierarchy(LoadDataFromDisk):
    def merge_contents_of_files(self, file_list):
        contents = list()
        all_yaml_individual = map(lambda x: yaml.load_all(open(x)), file_list)
        for configs in all_yaml_individual:
            for config in configs:
                contents.extend(config)
        return contents

    def load_contents_of_files(self):
        glob_pattern = os.path.join("hierarchy", "hierarchy.yaml")
        file_list = self.get_list_of_files(glob_pattern=glob_pattern, recursive=False)
        content = self.merge_contents_of_files(file_list=file_list)
        return content


class FilterApplicationsByHost:
    @staticmethod
    def get_applications_matching_host(applications, host_tags, host_name):
        # print(applications)
        filtered_applications = list()
        for application_name, application_values in applications.items():
            # print(host_name, host_tags)
            for tag_type, tag_values in host_tags.items():
                if tag_type in application_values:
                    # print("tag: %s, values: %s" % (tag_type, tag_values))
                    # print(tag_type in application_values, tag_type, application_values)
                    for tag_value in tag_values:
                        # print(tag_value in tag_values, tag_value, tag_values, application_values[tag_type])
                        if any(x == tag_value for x in application_values[tag_type]):
                            print("GOTYA! %s" % application_name)
                            filtered_applications.append(application_name)
        return filtered_applications


class LoadProperties(LoadDataFromDisk):
    def __init__(self, hierarchy, host_tags):
        self.host_tags = host_tags
        self.hierarchy = hierarchy
        self.regex_hierarchy = self.get_regex_hierarchy(hierarchy=hierarchy)

    def merge_contents_of_files(self, file_list):
        parser = configparser.ConfigParser(allow_no_value=True)
        for file_path in file_list:
            with open(file_path) as lines:
                lines = chain(("[default]",), lines)  # This line does the trick.
                parser.read_file(lines)

        contents = parser.items("default")
        return contents

    def load_contents_of_files(self):
        pass

    @staticmethod
    def get_regex_hierarchy(hierarchy):
        regex_hierarchy = []
        for hiera in hierarchy:
            regex_hiera = dict()
            regex_hiera['hiera'] = hiera
            regex_hiera['regex'] = "data/" + re.sub("\${.+?}", "([^/]+)", hiera)
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
        # print("START")
        for file_path in file_list:
            from pprint import pprint

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
                        elif hiera['tags'][i] in self.host_tags \
                                and hiera['tags'][i] in self.host_tags:
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
        glob_pattern = os.path.join("data", "**", file_name + ".properties")
        file_list = self.get_list_of_files(glob_pattern=glob_pattern, recursive=True)
        file_list_order_by_hierarchy = self.get_file_list_ordered_by_hierarchy(file_list=file_list,
                                                                               application_name=application_name,
                                                                               application_tags=application_tags)
        if file_list_order_by_hierarchy:
            content = self.merge_contents_of_files(file_list=file_list_order_by_hierarchy)
        return content

    def load_contents_of_property_list(self, application_name, application_tags):
        content = dict()
        for file_path in application_tags['properties']:
            result = self.load_contents_of_property_by_pattern(file_name=file_path,
                                                               application_name=application_name,
                                                               application_tags=application_tags)

            # if result:
            content[file_path] = result
        return content


class OutputProperties:

    def generate_file_by_host(self, configuration):
        result = False
        output_folder = os.path.join("output")
        for host_name, applications in configuration.items():
            for application_name, properties in applications.items():
                output_folder = os.path.join("output", host_name, application_name)
                if not os.path.exists(output_folder):
                    os.makedirs(output_folder)
                for property_name, keys in properties.items():
                    file_name = "%s.properties" % property_name

                    for key in keys:
                        with open(os.path.join(output_folder, file_name), 'w+') as out:
                            out.write("%s = %s" % (key[0], key[1]))

        return result

def main():
    hosts = LoadHosts().load_contents_of_files()
    applications = LoadApplications().load_contents_of_files()
    hierarchy = LoadHierarchy().load_contents_of_files()
    fa = FilterApplicationsByHost()

    all_properties = dict()
    processed = []
    for host_name, host_tags in hosts.items():
        print("\n\nHOST: ", host_name)
        # print("host tags: ", host_tags)
        filtered_applications = fa.get_applications_matching_host(applications=applications, host_tags=host_tags, host_name=host_name)
        print("FILTER", filtered_applications)
        host_properties = dict()
        processed.append(host_name)

        for application_name in filtered_applications:
            application_tags = applications[application_name]
            property_loader = LoadProperties(hierarchy=hierarchy, host_tags=host_tags)
            result = property_loader.load_contents_of_property_list(application_name=application_name,
                                                                    application_tags=application_tags)
            # if result:
            host_properties[application_name] = result

        # if host_properties:
        all_properties[host_name] = host_properties

    output = OutputProperties()
    output.generate_file_by_host(configuration=all_properties)
    from pprint import pprint
    # pprint(all_properties)


if __name__ == '__main__':
    main()
