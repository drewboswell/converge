from pyconverge.readers.BaseReader import BaseReader
import yaml
import glob
import os


class PropertiesReader(BaseReader):

    def __init__(self, **kwargs):
        self.hierarchy_path = kwargs.get("hierarchy_path")
        self.target_path = kwargs.get("target_path")
        self.repository_path = kwargs.get("repository_path")

    @staticmethod
    def get_list_of_files(glob_pattern, recursive=False):
        return glob.glob(glob_pattern, recursive=recursive)

    @staticmethod
    def merge_yaml_file_contents_hierarchy(file_list):
        contents = list()
        all_yaml_individual = map(lambda x: yaml.load_all(open(x)), file_list)
        for configs in all_yaml_individual:
            for config in configs:
                contents.extend(config)
        return contents

    @staticmethod
    def merge_yaml_file_contents_hosts(file_list):
        contents = dict()
        all_yaml_individual = map(lambda x: yaml.load_all(open(x)), file_list)
        for configs in all_yaml_individual:
            for config in configs:
                contents = {**contents, **config}
        return contents

    @staticmethod
    def merge_yaml_file_contents_applications(file_list):
        contents = dict()
        for file_path in file_list:
            app_name = file_path.rsplit("/", 1)[1][:-5]
            for config in yaml.load_all(open(file_path)):
                contents[app_name] = config
        return contents

    @staticmethod
    def get_applications_matching_host(applications, host_tags, host_name):
        filtered_applications = list()
        for application_name, application_values in applications.items():
            for tag_type, tag_values in host_tags.items():
                if tag_type in application_values:
                    for tag_value in tag_values:
                        if any(x == tag_value for x in application_values[tag_type]):
                            print("GOTYA! %s" % application_name)
                            filtered_applications.append(application_name)
        return filtered_applications

    def load_contents_of_hierarchy(self):
        print(self.hierarchy_path)
        print(os.path.isdir(self.hierarchy_path))
        glob_pattern = os.path.join(self.hierarchy_path, "hierarchy.yaml")
        file_list = self.get_list_of_files(glob_pattern=glob_pattern, recursive=False)
        content = self.merge_yaml_file_contents_hierarchy(file_list=file_list)
        return content

    def load_contents_of_hosts(self):
        glob_pattern = os.path.join(self.target_path, "hosts", "*.yaml")
        file_list = self.get_list_of_files(glob_pattern=glob_pattern, recursive=False)
        content = self.merge_yaml_file_contents_hosts(file_list=file_list)
        return content

    def load_contents_of_applications(self):
        glob_pattern = os.path.join(self.target_path, "applications", "*.yaml")
        file_list = self.get_list_of_files(glob_pattern=glob_pattern, recursive=False)
        content = self.merge_yaml_file_contents_applications(file_list=file_list)
        return content

    def read_hierarchy(self):
        return self.load_contents_of_hierarchy()

    def read_targets(self):
        targets = dict()
        targets["hosts"] = self.load_contents_of_hosts()
        targets["applications"] = self.load_contents_of_applications()
        return targets

    def read_repository(self):
        repository = dict()
        return repository


def main():
    args = {"hierarchy_path": "/home/drew/workspace/converge/tests/resources/repository/hierarchy",
            "target_path": "/home/drew/workspace/converge/tests/resources/repository/targets",
            "repository_path": "/home/drew/workspace/converge/tests/resources/repository/data"}
    lol = PropertiesReader(**args)
    hierarchy = lol.read_hierarchy()
    targets = lol.read_targets()
    hosts = targets['hosts']
    applications = targets['applications']
    for host in hosts.items():
        print(host)
        fa = lol.get_applications_matching_host(applications=applications, host_tags=host[1], host_name=host[0])
        break
    print(applications)
    print(fa)

if __name__ == '__main__':
    main()

