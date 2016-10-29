import configparser
import os
import time
import logging
from pprint import pprint
from BaseFunctions import BaseFunctions

logging.basicConfig(level=logging.DEBUG)
statistics = dict()
statistics['start_time'] = time.time()

config_path = "../tests/resources/etc/converge.ini"
config = configparser.ConfigParser()
config.read(config_path)

repository_path = config['DEFAULT']['repository_path']

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

cv = BaseFunctions(repository_path=repository_path,
                   node_path=node_path,
                   node_group_path=node_group_path,
                   package_path=package_path,
                   application_path=application_path,
                   logger=logging)

cv.resolve_node_groups()

# statistics calculations
statistics["end_time"] = time.time()
statistics["total_time"] = statistics["end_time"] - statistics['start_time']

print(statistics["total_time"])
