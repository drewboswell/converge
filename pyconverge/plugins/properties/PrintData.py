# -*- coding: utf-8 -*-

import logging


class PrintHostTags:
    @staticmethod
    def run(data, conf, **kwargs):
        for host_name in data.targets["hosts"]:
            message = "HOST TAG LOOKUP \n %s tags:\n\t%s"
            if host_name in data.data["hosts"]:
                host_tags = data.data["hosts"][host_name]
                logging.info(message % (host_name, str(host_tags)))
        return data


class PrintHostApplications:
    @staticmethod
    def run(data, conf, **kwargs):
        message = "HOST TO APPLICATION LOOKUP \n HOST: %s has applications:\n\t%s"
        host_name = kwargs.get("host_name")
        logging.info(message % (host_name, data.targets["applications"]))
        return data