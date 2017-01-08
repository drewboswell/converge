from pyconverge.plugins.BasePlugin import BasePlugin
from .LoadTargets import LoadHierarchy, LoadHosts, LoadApplications
from .Filters import FilterApplicationsByHost
from .LoadProperties import LoadProperties


class PropertiesPlugin(BasePlugin):
    def __init__(self, **kwargs):
        self.hierarchy_path = kwargs.get("hierarchy_path")
        self.target_path = kwargs.get("target_path")
        self.repository_path = kwargs.get("repository_path")
        self.hierarchy = list()
        self.targets = dict()

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
            self.resolve_target_data(target=host, periodic_write=periodic_write)

        if not periodic_write:
            self.write_all_data(resolved_data=resolved_data)
        return resolved_data

    def resolve_target_data(self, target, periodic_write=False):
        resolved_data = dict()
        filters = FilterApplicationsByHost()
        host_tags = target[1]
        properties = dict()
        filtered_applications = filters.get_applications_matching_host(applications=self.targets["applications"],
                                                                       host_tags=host_tags)
        for application in filtered_applications:
            application_tags = self.targets["applications"][application]
            property_loader = LoadProperties(hierarchy=self.hierarchy, host_tags=host_tags)
            result = property_loader.load_contents_of_property_list(application_name=application,
                                                                    application_tags=application_tags)

            print(result)
            if result:
                resolved_data[application] = result
        print(resolved_data)
        if periodic_write:
            self.write_target_data(resolved_data=resolved_data)

        return resolved_data

    def write_all_data(self, resolved_data):
        return False

    def write_target_data(self, resolved_data):
        return False


def main():
    args = {"hierarchy_path": "/home/drew/workspace/converge/tests/resources/repository/hierarchy",
            "target_path": "/home/drew/workspace/converge/tests/resources/repository/targets",
            "repository_path": "/home/drew/workspace/converge/tests/resources/repository/data"}
    lol = PropertiesPlugin(**args)
    lol.read_hierarchy()
    lol.read_targets()
    hosts = lol.targets['hosts']
    applications = lol.targets['applications']
    # print(lol.hierarchy)
    # print(hosts)
    # print(applications)
    for host in hosts.items():
        fa = lol.resolve_target_data(target=host)
        break
        # print(applications)


if __name__ == '__main__':
    main()
