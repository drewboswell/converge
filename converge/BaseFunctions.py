import glob
import yaml
import sys
import os
import time


class BaseFunctions:
    """
    this class holds the basic file manipulation, resolving and miscellaneous functions used by converge
    """

    def __init__(self, repository_path, node_path, node_group_path, package_path, application_path, hierarchy_path,
                 package_recursion_depth_max, logger):
        self.repository_path = repository_path
        self.node_path = node_path
        self.node_group_path = node_group_path
        self.package_path = package_path
        self.application_path = application_path
        self.hierarchy_path = hierarchy_path
        self.package_recursion_depth_max = package_recursion_depth_max

        self.logging = logger
        self.statistics = {}

        self.non_resolved_configuration = self.load_non_resolved_configuration()

        self.nodes = dict()
        self.node_groups = dict()
        self.packages = dict()
        self.applications = dict()
        self.hierarchy = dict()
        # self.node_applications allows connection between nodes -> application, also limits useless host lookups
        # (avoids full iteration where not necessary)
        self.node_applications = dict()

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
        non_resolved_configuration['hierarchy'] = self.load_yaml_files_in_directory(directory=self.hierarchy_path)
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
                        and not (node_group[0] in self.node_groups
                                 and node_group[1] in self.node_groups[node_group[0]]):
                    self.logging.fatal("Did not find node_group or node by "
                                       "coordinates: %s/%s" % (node_group[0], node_group[1]))
                    sys.exit(1)
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

    def verify_application_package(self, package_name):
        result = False
        if package_name in self.packages:
            result = True
        else:
            self.logging.error("Package does not exist '%s' or has no keys defined" % package_name)
            sys.exit(1)
        return result

    def verify_application_node_group(self, node_group_name, application_name):
        node_group_coordinates = node_group_name.split("::")
        if node_group_coordinates[0] in self.node_groups \
                and node_group_coordinates[1] in self.node_groups[node_group_coordinates[0]]:
            for node in self.node_groups[node_group_coordinates[0]][node_group_coordinates[1]]:
                if node not in self.node_applications:
                    self.node_applications[node] = set()
                if application_name in self.node_applications[node]:
                    self.logging.warning("key-value collision possible! "
                                         "Application '%s' already referenced on node %s, " % (application_name, node))
                self.node_applications[node].add(application_name)
        else:
            self.logging.error("Node Group does not exist '%s' "
                               "referenced by application '%s'" % (node_group_name, application_name))
            sys.exit(1)

    def verify_application_package_key_override(self, key_coordinates, values):
        result = False

        key = key_coordinates.split("::", 1)
        if key[0] in self.packages and key[1] in self.packages[key[0]]:
            if self.verify_value_references(values=values):
                result = True
        else:
            self.logging.error("Override Coordinates don't exist for %s/%s" % (key[0], key[1]))
            sys.exit(1)

        return result

    def resolve_application(self, application_name, application):
        time_marker = time.time()
        result = dict()
        result["packages"] = []
        result["package_overrides"] = dict()

        time_market2 = time.time()
        for package_name in application["package::dependencies"]:
            if self.verify_application_package(package_name=package_name):
                result["packages"].append(package_name)
        self.statistics["resolve_application_%s_packages" % application_name] = time.time() - time_market2

        time_market2 = time.time()
        for node_group_name in application["node_group::dependencies"]:
            self.verify_application_node_group(node_group_name=node_group_name, application_name=application_name)
        self.statistics["resolve_application_%s_node_groups" % application_name] = time.time() - time_market2

        time_market2 = time.time()
        for key_coordinates, values in application["package::key::overrides"].items():
            if self.verify_application_package_key_override(key_coordinates=key_coordinates, values=values):
                result["package_overrides"][key_coordinates] = values

        self.statistics["resolve_application_%s_package_overrides" % application_name] = time.time() - time_market2

        self.applications[application_name] = result
        self.statistics["resolve_application_%s" % application_name] = time.time() - time_marker
        return result

    def resolve_applications(self):
        time_marker = time.time()

        for application_name, application in self.non_resolved_configuration["applications"].items():
            self.logging.debug("Application '%s' processing started" % application_name)
            self.resolve_application(application_name=application_name, application=application)

        self.statistics['resolve_applications'] = time.time() - time_marker

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

    def get_hierarchy_path(self):
        return self.hierarchy_path

    def get_nodes(self):
        return self.nodes

    def get_node_groups(self):
        return self.node_groups

    def get_packages(self):
        return self.packages

    def get_applications(self):
        return self.applications

    def get_hierarchy(self):
        return self.hierarchy

    def get_node_applications(self):
        return self.node_applications

    def get_statistics(self):
        # update totals
        self.statistics["nodes_total"] = len(self.get_nodes())
        self.statistics["node_groups_total"] = len(self.get_node_groups())
        self.statistics["applications_total"] = len(self.get_applications())
        self.statistics["packages_total"] = len(self.get_packages())
        self.statistics["node_applications_total"] = len(self.get_node_applications())
        return self.statistics
