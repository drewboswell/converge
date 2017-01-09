# -*- coding: utf-8 -*-

import os


class OutputProperties:

    def __init__(self, output_path="output"):
        self.output_path = output_path

    def generate_files_by_target(self, configuration):
        result = False
        for host_name, applications in configuration.items():
            for application_name, properties in applications.items():
                output_folder = os.path.join(self.output_path, host_name, application_name)
                if not os.path.exists(output_folder):
                    os.makedirs(output_folder)
                for property_name, keys in properties.items():
                    file_name = "%s.properties" % property_name
                    for key in keys:
                        with open(os.path.join(output_folder, file_name), 'w+') as out:
                            out.write("%s = %s" % (key[0], key[1]))

        return result
