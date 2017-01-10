# -*- coding: utf-8 -*-

from importlib import import_module
import logging

log = logging.getLogger(__name__)


# Dynamically import libraries based on user preferences
def get_dynamic_class(finder_path):
    module_name, class_name = finder_path.rsplit('.', 1)
    module = import_module(module_name)
    log.debug("Imported Modeule %s, Class %s" % (module_name, class_name))
    return getattr(module, class_name)


class BaseClassLoader:
    def __init__(self, settings):
        self.dynamic_classes = dict()

        # Load all classes into context for reading, resolving and writing
        for dynamic_class_type in ["plugins"]:
            dynamic_classes = [get_dynamic_class(dynamic_class_type_path)
                               for dynamic_class_type_path
                               in settings[dynamic_class_type].split(",")]
            self.dynamic_classes[dynamic_class_type] = dynamic_classes

    def run_plugins(self, **kwargs):
        loaded_data = dict()
        for plugin in self.dynamic_classes["plugins"]:
            log.info("Plugin Class %s initializing" % plugin)
            plugin_impl = plugin(**kwargs)
            plugin_impl.read_hierarchy()
            plugin_impl.read_targets()
            resolved_data = plugin_impl.resolve_all_data(periodic_write=False)
            plugin_impl.write_data(resolved_data=resolved_data)
        return loaded_data

    def run_validators(self):
        validation_data = dict()
        for validator in self.dynamic_classes["validators"]:
            log.info("Validation Class %s initializing" % validator)
            validation = validator.validate()
            validation_data[validator] = validation
        return validation_data

    def run_readers(self):
        loaded_data = dict()
        for reader in self.dynamic_classes["readers"]:
            log.info("Reader Class %s initializing" % reader)
            read_data = reader.read_data()
            for read_filter in self.dynamic_classes["read_filters"]:
                log.info("Post Read Filter Class %s initializing" % read_filter)
                read_data = read_filter.filter_data(read_data=read_data)
            loaded_data[reader] = read_data
        return loaded_data

    def run_resolvers(self, unresolved_data):
        resolved_data = dict()
        for resolver in self.dynamic_classes["resolvers"]:
            log.info("Resolver Class %s initializing" % resolver)
            resolved_data[resolver] = resolver.resolve_data(unresolved_data=unresolved_data)
        return resolved_data

    def run_writers(self, resolved_data):
        written_data = dict()
        for writer in self.dynamic_classes["readers"]:
            for write_filter in self.dynamic_classes["write_filters"]:
                log.info("Pre Write Filter Class %s initializing" % write_filter)
                resolved_data = write_filter.filter_data(resolved_data=resolved_data)
            log.info("Writer Class %s initializing" % writer)
            written_data[writer] = writer.write_data(resolved_data=resolved_data)
