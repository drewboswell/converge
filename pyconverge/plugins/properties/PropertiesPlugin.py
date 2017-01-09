# -*- coding: utf-8 -*-

from pyconverge.plugins.BasePlugin import BasePlugin
from .LoadTargets import LoadHierarchy, LoadHosts, LoadApplications
from .Filters import FilterApplicationsByHost
from .LoadProperties import LoadProperties
from .OutputProperties import OutputProperties
import logging


class PropertiesPlugin(BasePlugin):
    def __init__(self, **kwargs):
        self.hierarchy_path = kwargs.get("hierarchy")
        self.target_path = kwargs.get("target")
        self.repository_path = kwargs.get("data")
        self.hierarchy = list()
        self.targets = dict()
        self.output = OutputProperties(output_path=kwargs.get("output"))

    def read_hierarchy(self):
        hiera_loader = LoadHierarchy()
        self.hierarchy = hiera_loader.load_contents_of_files(base_directory=self.hierarchy_path)

    def read_targets(self):
        targets = dict()
        # load hosts
        hosts = LoadHosts()
        targets["hosts"] = hosts.load_contents_of_files(base_directory=self.target_path)
        # load applications
        applications = LoadApplications()
        targets["applications"] = applications.load_contents_of_files(base_directory=self.target_path)
        self.targets = targets

    def read_repository(self):
        repository = dict()
        return repository

    def resolve_all_data(self, periodic_write=False):
        resolved_data = dict()

        for host in self.targets["hosts"]:
            resolved_data[host] = self.resolve_target_data(target_name=host, periodic_write=periodic_write)

        return resolved_data

    def resolve_target_data(self, target_name, periodic_write=False):
        resolved_data = dict()
        filters = FilterApplicationsByHost()
        host_tags = self.targets["hosts"][target_name]
        filtered_applications = filters.get_applications_matching_host(applications=self.targets["applications"],
                                                                       host_tags=host_tags)
        lines = 0
        for application in filtered_applications:
            application_tags = self.targets["applications"][application]
            property_loader = LoadProperties(hierarchy=self.hierarchy,
                                             host_tags=host_tags,
                                             repository_path=self.repository_path)
            result = property_loader.load_contents_of_property_list(application_name=application,
                                                                    application_tags=application_tags)
            if result:
                lines += len(result)
                resolved_data[application] = result

        logging.info("Generating data for target: %-15s (files: %-3i, lines: %3i)" % (target_name,
                                                                                len(resolved_data),
                                                                                lines))
        if periodic_write:
            self.write_data(resolved_data=resolved_data)

        return resolved_data

    def write_data(self, resolved_data):
        return self.output.generate_files_by_target(configuration=resolved_data)
