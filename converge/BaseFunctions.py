import glob
import yaml
import sys
import os


class BaseFunctions:
    """
    this class holds the basic file manipulation, resolving and miscellaneous functions used by converge
    """

    def __init__(self, repository_path, node_path, node_group_path, package_path, application_path, logger):
        self.repository_path = repository_path
        self.node_path = node_path
        self.node_group_path = node_group_path
        self.package_path = package_path
        self.application_path = application_path

        self.logging = logger

        self.non_resolved_configuration = self.load_non_resolved_configuration()
        self.nodes = self.load_yaml_files_in_directory(directory=self.node_path)
        self.node_groups = dict()
        self.packages = dict()
        self.applications = dict()

    def load_yaml_files_in_directory(self, directory):
        result = dict()
        self.logging.info("Loading YAML Folder: %s" % directory)
        for filename_path in glob.iglob(os.path.join(directory, "*.yaml"), recursive=False):
            with open(filename_path, 'r') as f:
                filename_exploded = filename_path.split("/")
                filename = filename_exploded[-1][:-5]
                result[filename] = yaml.safe_load(f)
                self.logging.info("Loaded YAML file: %s.yaml" % filename)
        return result

    def load_non_resolved_configuration(self):
        non_resolved_configuration = dict()
        non_resolved_configuration['nodes'] = self.load_yaml_files_in_directory(directory=self.node_path)
        non_resolved_configuration['node_groups'] = self.load_yaml_files_in_directory(directory=self.node_group_path)
        non_resolved_configuration['packages'] = self.load_yaml_files_in_directory(directory=self.package_path)
        non_resolved_configuration['applications'] = self.load_yaml_files_in_directory(directory=self.application_path)

        return non_resolved_configuration

    def resolve_node_group(self, node_group, nodes):
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
                                nodules.extend(nodes)
                            else:
                                nodules.extend(self.non_resolved_configuration
                                               ["node_groups"]
                                               [components[0]]
                                               [components[1]])
                        else:
                            self.logging.error("node_group '%s' inception not activated, you are "
                                               "not allowed to use references. Exiting" % node_group)
                            sys.exit(1)
                    elif nodule in nodes:
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
        # Resolve nodes in node_groups
        for node_group_name, node_group in self.non_resolved_configuration["node_groups"].items():
            self.logging.info("Starting Node Group file processing for %s" % node_group_name)
            nodes = self.non_resolved_configuration["nodes"]["nodes"]
            self.resolve_node_group(node_group=node_group, nodes=nodes)

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
        return self.application_path

    def get_node_groups(self):
        return self.node_groups

    def get_packages(self):
        return self.packages

    def get_applications(self):
        return self.applications
