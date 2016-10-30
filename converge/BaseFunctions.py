import glob
import yaml
import sys
import os
import time


class BaseFunctions:
    """
    this class holds the basic file manipulation, resolving and miscellaneous functions used by converge
    """

    def __init__(self, repository_path, node_path, node_group_path, package_path, application_path,
                 package_recursion_depth_max, logger):
        self.repository_path = repository_path
        self.node_path = node_path
        self.node_group_path = node_group_path
        self.package_path = package_path
        self.application_path = application_path
        self.package_recursion_depth_max = package_recursion_depth_max

        self.logging = logger
        self.statistics = {}

        self.non_resolved_configuration = self.load_non_resolved_configuration()

        self.nodes = dict()
        self.node_groups = dict()
        self.packages = dict()
        self.applications = dict()

    def load_yaml_files_in_directory(self, directory):
        time_marker = time.time()
        result = dict()
        self.logging.info("Loading YAML Folder: %s" % directory)
        for filename_path in glob.iglob(os.path.join(directory, "*.yaml"), recursive=False):
            with open(filename_path, 'r') as f:
                filename_exploded = filename_path.split("/")
                filename = filename_exploded[-1][:-5]
                result[filename] = yaml.load(f)
                self.logging.info("Loaded YAML file: %s.yaml" % filename)

        self.statistics['load_yaml_files_%s' % directory.split("/")[-1]] = time.time() - time_marker
        return result

    def load_non_resolved_configuration(self):
        time_marker = time.time()
        non_resolved_configuration = dict()
        non_resolved_configuration['nodes'] = self.load_yaml_files_in_directory(directory=self.node_path)
        non_resolved_configuration['node_groups'] = self.load_yaml_files_in_directory(directory=self.node_group_path)
        non_resolved_configuration['packages'] = self.load_yaml_files_in_directory(directory=self.package_path)
        non_resolved_configuration['applications'] = self.load_yaml_files_in_directory(directory=self.application_path)
        self.statistics['load_yaml_all'] = time.time() - time_marker
        return non_resolved_configuration

    def resolve_nodes(self):
        time_marker = time.time()
        self.nodes = self.non_resolved_configuration['nodes']['nodes']
        self.statistics['resolve_nodes'] = time.time() - time_marker

    def resolve_node_group(self, node_group):
        result = dict()
        nodes_encountered = []

        # Todo: maybe add the possibility to add a base type (other than nodes? or on the fly types?)
        # base_type = node_group["node_group::config"]["base_type"] == True
        allow_duplicates = node_group["node_group::config"]["allow_duplicates"] == True
        allow_inception = node_group["node_group::config"]["allow_inception"] == True

        for group_name, group in node_group.items():
            if group_name != "node_group::config":
                nodules = []
                self.logging.info("node_group '%s' STARTING processing" % group_name)
                for nodule in group:
                    if "::" in nodule:
                        if allow_inception:
                            self.logging.debug("node_group '%s' RESOLVING: %s" % (group_name, nodule))
                            components = nodule.split("::")
                            if "nodes::nodes" in nodule:
                                nodules.extend(self.nodes)
                            else:
                                nodules.extend(self.non_resolved_configuration
                                               ["node_groups"]
                                               [components[0]]
                                               [components[1]])
                        else:
                            self.logging.error("node_group '%s' inception not activated, you are "
                                               "not allowed to use references. Exiting" % node_group)
                            sys.exit(1)
                    elif nodule in self.nodes:
                        nodules.append(nodule)
                    else:
                        self.logging.error("node_group '%s' Node %s not found. Exiting" % (node_group, nodule))
                        sys.exit(1)

                if allow_duplicates is False:
                    for node in nodules:
                        if any(node == x for x in nodes_encountered):
                            self.logging.error(
                                "Node reuse is not allowed for node_group '%s' [host: '%s']" % (group_name, node))
                            sys.exit(1)
                        else:
                            nodes_encountered.append(node)
                self.logging.info("node_group '%s' FINISHED processing, found %i nodes" % (group_name, len(nodules)))
                result[group_name] = set(nodules)

        return result

    def resolve_node_groups(self):
        time_marker = time.time()
        # Resolve nodes in node_groups
        for node_group_name, node_group in self.non_resolved_configuration["node_groups"].items():
            self.logging.info("Starting Node Group file processing for %s" % node_group_name)
            time_marker2 = time.time()
            self.node_groups[node_group_name] = self.resolve_node_group(node_group=node_group)
            self.statistics['resolve_node_group_%s' % node_group_name] = time.time() - time_marker2
        self.statistics['resolve_node_groups'] = time.time() - time_marker

    def resolve_key_extension(self, key_map, depth):
        time_marker = time.time()
        key = key_map.split("::", 1)
        if key[0] in self.packages and key[1] in self.packages[key[0]]:
            result = self.packages[key[0]]
        else:
            package = self.non_resolved_configuration["packages"][key[0]]
            result = self.resolve_package(package=package, package_name=key[0], depth=depth + 1)
            if key[1] not in result:
                self.logging.error(
                    "KEY MAP %s/%s not resolvable, reference package or key does not exist" % (key[0], key[1]))
                sys.exit(1)
        self.statistics['resolve_key_extension_%s_%s' % (key_map[0], key_map[1])] = time.time() - time_marker
        return result[key[1]]

    def verify_value_references(self, values):
        result = True

        for hierarchy, value in values.items():
            if hierarchy != "default":
                node_group = hierarchy.split("::", 1)
                if not (node_group[0] == "nodes" and node_group[1] in self.nodes) \
                        and not (
                                node_group[0] in self.node_groups and node_group[1] in self.node_groups[node_group[0]]):
                    self.logging.error(
                        "Did not find node_group or node by coordinates: %s/%s" % (node_group[0], node_group[1]))
                    result = False
        return result

    def resolve_package(self, package, package_name, depth=1):
        time_marker = time.time()
        result = dict()
        keys_encountered = []

        if depth < self.package_recursion_depth_max:
            for key, values in package.items():
                if key not in keys_encountered:
                    self.logging.debug("Processing KEY %s" % key)
                    keys_encountered.append(key)
                    resolved_values = {}
                    if "extend" in values:
                        resolved_values.update(self.resolve_key_extension(values['extend'], depth=depth))
                        values.pop("extend")

                    resolved_values.update(values)
                    if self.verify_value_references(values):
                        result[key] = resolved_values
                    else:
                        self.logging.error("node_group check on key overrides failed, exiting")
                        sys.exit(1)
            self.packages[package_name] = result
        else:
            self.logging.error("MAX Depth has been exceeded")
        self.statistics['resolve_package_%s' % package_name] = time.time() - time_marker
        return result

    def resolve_packages(self):
        time_marker = time.time()
        # Resolve package in packages
        for package_name, package in self.non_resolved_configuration["packages"].items():
            self.logging.info("PACKAGE '%s' processing started" % package_name)
            if package:
                self.resolve_package(package=package, package_name=package_name)
        self.statistics['resolve_packages'] = time.time() - time_marker

    # get class variables functions
    def get_non_resolved_configuration(self):
        return self.non_resolved_configuration

    def get_node_path(self):
        return self.node_path

    def get_node_group_path(self):
        return self.node_path

    def get_package_path(self):
        return self.package_path

    def get_application_path(self):
        return self.application_path

    def get_nodes(self):
        return self.nodes

    def get_node_groups(self):
        return self.node_groups

    def get_packages(self):
        return self.packages

    def get_applications(self):
        return self.applications

    def get_statistics(self):
        return self.statistics
