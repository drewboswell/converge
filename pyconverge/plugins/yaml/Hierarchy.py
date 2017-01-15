from .LoadDataFromDisk import LoadDataFromDisk
import yaml
import os


class Hierarchy(LoadDataFromDisk):

    def __init__(self, settings):
        self.conf = settings["yaml"]

    def merge_contents_of_files(self, file_list):
        contents = list()
        all_yaml_individual = map(lambda x: yaml.load_all(open(x)), file_list)
        for configs in all_yaml_individual:
            for config in configs:
                contents.extend(config)
        return contents

    def read_data(self):
        glob_pattern = os.path.join(self.conf["base_dir"], self.conf["hierarchy_path"])
        file_list = self.get_list_of_files(glob_pattern=glob_pattern, recursive=False)
        content = self.merge_contents_of_files(file_list=file_list)
        return content


