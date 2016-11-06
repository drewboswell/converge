# -*- coding: utf-8 -*-

import configparser
import os
import time
import logging
from pprint import pprint
from .BaseFunctions import BaseFunctions


# add main entry point
def main():

    # Figure out where we're installed
    bin_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(bin_dir)
    conf_dir = os.path.join(root_dir, 'conf')

    statistics = dict()
    statistics['start_time'] = time.time()

    config_path = os.path.join(conf_dir,"converge.ini")
    config = configparser.ConfigParser()
    config.read(config_path)

    # set path for nodes
    if "logging_level" in config['DEFAULT']:
        logging_level = config["DEFAULT"]["logging_level"]
    else:
        logging_level = "INFO"

    logging.basicConfig(level=logging_level)

    # set path for repository
    if "repository_path" in config['DEFAULT']:
        repository_path = config["DEFAULT"]["repository"]
    else:
        repository_path = os.path.join(root_dir, "repository")

    # set path for nodes
    if "node_path" in config['DEFAULT']:
        node_path = config["DEFAULT"]["node_path"]
    else:
        node_path = os.path.join(repository_path, "nodes")

    # set path for node_groups
    if "node_group_path" in config['DEFAULT']:
        node_group_path = config["DEFAULT"]["node_group_path"]
    else:
        node_group_path = os.path.join(repository_path, "node_groups")

    # set path for packages
    if "package_path" in config['DEFAULT']:
        package_path = config["DEFAULT"]["package_path"]
    else:
        package_path = os.path.join(repository_path, "packages")

    # set path for applications
    if "application_path" in config['DEFAULT']:
        application_path = config["DEFAULT"]["application_path"]
    else:
        application_path = os.path.join(repository_path, "applications")

    # set path for hierarchy
    if "hierarchy_path" in config['DEFAULT']:
        hierarchy_path = config["DEFAULT"]["hierarchy_path"]
    else:
        hierarchy_path = os.path.join(repository_path, "hierarchy")

    # set recursion depth on package resolution
    if "package_recursion_depth_max" in config['DEFAULT']:
        package_recursion_depth_max = config["DEFAULT"]["package_recursion_depth_max"]
    else:
        package_recursion_depth_max = 7


    cv = BaseFunctions(repository_path=repository_path,
                       node_path=node_path,
                       node_group_path=node_group_path,
                       package_path=package_path,
                       application_path=application_path,
                       hierarchy_path=hierarchy_path,
                       package_recursion_depth_max=package_recursion_depth_max,
                       logger=logging)

    cv.resolve_nodes()
    cv.resolve_node_groups()
    cv.resolve_packages()
    cv.resolve_applications()
    #cv.resolve_hierarchy()

    #pprint(cv.get_non_resolved_configuration()['packages'])
    # statistics calculations
    statistics["end_time"] = time.time()
    statistics["total_time"] = statistics["end_time"] - statistics['start_time']

    statistics.update(cv.get_statistics())

    logging.info(statistics)
    logging.info("Finished Run in total of '%s' seconds" % statistics["total_time"])

    # Todo: add the ability to do AND(/OR?) operations on node_group overrides?
    # Todo: add the ability to extend a pre-existing package (import keys etc)
    # Todo: allow inception in package values (if you write take value from another key ${::}?)