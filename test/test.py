import glob
import configparser
import os
import sys
import yaml
import time
from pprint import pprint

statistics = dict()
statistics['start_time'] = time.time()

config = configparser.ConfigParser()
config.read("resources/etc/converge.ini")


def load_yaml_files_in_directory(directory):
    result = dict()
    for filename_path in glob.iglob(os.path.join(directory, "*.yaml"), recursive=False):
        with open(filename_path, 'r') as f:
            filename_exploded = filename_path.split("/")
            filename = filename_exploded[-1][:-5]
            result[filename] = yaml.safe_load(f)
    return result


def resolve_node_group(node_group, nodes, non_resolved_configuration):
    result = dict()

    all_nodes_encountered = []

    # Todo: maybe add the possibility to add a base type (other than nodes? or on the fly types?)
    # base_type = node_group["node_group::config"]["base_type"] == True
    allow_duplicates = node_group["node_group::config"]["allow_duplicates"] == True
    allow_inception = node_group["node_group::config"]["allow_inception"] == True

    for group_name, group in node_group.items():
        if group_name != "node_group::config":
            nodules = []
            for nodule in group:
                if "::" in nodule:
                    if allow_inception:
                        print("RESOLVING: %s" % nodule)
                        components = nodule.split("::")
                        if "nodes::nodes" in nodule:
                            nodules.extend(nodes)
                        else:
                            nodules.extend(non_resolved_configuration["node_groups"][components[0]][components[1]])
                    else:
                        print("ERROR: inception not activated, you are not allowed to use references. exiting")
                        sys.exit(1)
                elif nodule in nodes:
                    nodules.append(nodule)
                else:
                    print("ERROR: Node %s not found" % nodule)

            if allow_duplicates is False:
                print(nodules)
                print(all_nodes_encountered)
                for node in nodules:
                    if any(node == x for x in all_nodes_encountered):
                        print("ERROR: Node reuse is not allowed for node_group '%s' [host: '%s']" % (group_name, node))
                        sys.exit(1)
                    else:
                        all_nodes_encountered.append(node)

            result[group_name] = set(nodules)

    return result


repository_path = config['DEFAULT']['repository_path']

non_resolved_configuration = dict()
resolved_configuration = dict()

# load all nodes
if "node_path" in config['DEFAULT']:
    node_path = config["DEFAULT"]["node_path"]
else:
    node_path = os.path.join(repository_path, "nodes")
non_resolved_configuration['nodes'] = load_yaml_files_in_directory(directory=node_path)

# load all node_groups
if "node_group_path" in config['DEFAULT']:
    node_group_path = config["DEFAULT"]["node_group_path"]
else:
    node_group_path = os.path.join(repository_path, "node_groups")
non_resolved_configuration['node_groups'] = load_yaml_files_in_directory(directory=node_group_path)

# load all packages
if "package_path" in config['DEFAULT']:
    package_path = config["DEFAULT"]["package_path"]
else:
    package_path = os.path.join(repository_path, "packages")
non_resolved_configuration['packages'] = load_yaml_files_in_directory(directory=package_path)

# load all applications
if "application_path" in config['DEFAULT']:
    application_path = config["DEFAULT"]["application_path"]
else:
    application_path = os.path.join(repository_path, "applications")
non_resolved_configuration['applications'] = load_yaml_files_in_directory(directory=application_path)


# Resolve nodes in node_groups
for node_group_name, node_group in non_resolved_configuration["node_groups"].items():
    print("\n#", node_group_name)
    pprint(resolve_node_group(node_group=node_group,
                              nodes=non_resolved_configuration["nodes"]["nodes"],
                              non_resolved_configuration=non_resolved_configuration))

# statistics calculations
statistics["end_time"] = time.time()
statistics["total_time"] = statistics["end_time"] - statistics['start_time']

print(statistics["total_time"])

# pprint(resolved_configuration)
