# -*- coding: utf-8 -*-

import os
import logging
import sys


class WriteHostApplicationPropertiesToFiles:
    @staticmethod
    def run(data, conf, **kwargs):
        host_name = kwargs.get("host_name")
        application_name = kwargs.get("application_name")
        output_dir = conf["programs"]["resolve"]["conf"]["properties"]["output_dir"]
        logging.info("Generating files for application %s on host %s" % (application_name, host_name))
        output_folder = os.path.join(output_dir, host_name, application_name)
        if not os.path.isdir(output_folder):
            os.makedirs(output_folder)

        for file_name, properties in data.data["file_data"].items():
            logging.info("Writing File: %s.properties" % file_name)
            for property in properties:
                with open(os.path.join(output_folder, file_name+".properties"), 'w+') as out:
                    out.write("%s = %s" % (property[0], property[1]))

        return data
