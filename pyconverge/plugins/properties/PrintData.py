# -*- coding: utf-8 -*-

import logging


class PrintHostTags:
    @staticmethod
    def run(data, **kwargs):
        for host_name in data.targets["hosts"]:
            message = "HOST TAG LOOKUP \n %s tags:\n\t%s"
            if host_name in data.data["hosts"]:
                host_tags = data.data["hosts"][host_name]
                logging.info(message % (host_name, str(host_tags)))
        return data


class PrintHostApplications:
    @staticmethod
    def run(data, **kwargs):
        message = "HOST TO APPLICATION LOOKUP \n HOST: %s has applications:\n\t%s"
        host_name = kwargs.get("host_name")
        logging.info(message % (host_name, data.targets["applications"]))
        return data


class PrintTagHosts:
    @staticmethod
    def run(data, **kwargs):
        message = "TAG TO HOST LOOKUP \n TAG: %s=%s has hosts:\n\t%s"
        tag_name = kwargs.get("tag_name")
        tag_value = kwargs.get("tag_value")
        logging.info(message % (tag_name, tag_value, list(data.targets["hosts"])))
        return data


class PrintTagApplications:
    @staticmethod
    def run(data, **kwargs):
        message = "TAG TO APPLICATION LOOKUP \n TAG: %s=%s has applications:\n\t%s"
        tag_name = kwargs.get("tag_name")
        tag_value = kwargs.get("tag_value")
        logging.info(message % (tag_name, tag_value, data.targets["applications"]))
        return data


class PrintApplicationHosts:
    @staticmethod
    def run(data, **kwargs):
        message = "APPLICATION TO HOST LOOKUP \n APPLICATION: %s has hosts:\n\t%s"
        application_name = kwargs.get("application_name")
        logging.info(message % (application_name, data.targets["hosts"]))
        return data


class PrintApplicationTags:
    @staticmethod
    def run(data, **kwargs):
        message = "APPLICATION TO TAG LOOKUP \n APPLICATION: %s has tags:\n\t%s"
        application_name = kwargs.get("application_name")
        logging.info(message % (application_name, data.data["application_hosts"][application_name]))
        return data


class PrintApplicationProperties:
    @staticmethod
    def run(data, **kwargs):
        message = "APPLICATION TO PROPERTIES LOOKUP \n APPLICATION: %s has properties:\n\t%s"
        appliation_name = kwargs.get("application_name")
        logging.info(message % (appliation_name, list(data.data["application_properties"][appliation_name]["properties"])))
        return data


class PrintPropertyApplications:
    @staticmethod
    def run(data, **kwargs):
        message = "PROPERTIES TO APPLICATION LOOKUP \n PROPERTIES: %s has applications:\n\t%s"
        property_name = kwargs.get("property_name")
        logging.info(message % (property_name, data.targets["applications"]))
        return data
