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


class ConvergeData(object):
    validation = dict()
    hierarchy = dict()
    data = dict()


class BaseClassLoader:
    def __init__(self, settings):
        self.programs = settings["programs"]
        self.settings = dict()
        self.instructions = list()

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

    def run_instruction_set(self, **kwargs):
        result = False
        data = ConvergeData()
        program_name = kwargs.get("program")
        self.instructions = self.programs[program_name]["instructions"]
        self.settings = self.programs[program_name]["conf"]

        for instruction_block in self.instructions:
            for instruction_type, instructions in instruction_block.items():
                for instruction in instructions:
                    # if instruction_type == "validate":
                    #     data.validation[instruction] = self.run_validator(dynamic_class=instruction)
                    # elif instruction_type == "read_data":
                    #     data.data[instruction] = self.run_reader(dynamic_class=instruction)
                    if instruction_type == "read_hierarchy":
                        print(instruction)
                        data.hierarchy[instruction] = self.run_reader(dynamic_class=instruction)

        print(data.hierarchy)
        return result

    def run_validator(self, dynamic_class):
        validator = get_dynamic_class(finder_path=dynamic_class)
        log.info("Validation Class %s initializing" % validator)
        validation = validator.validate()
        return validation

    def run_reader(self, dynamic_class):
        reader = get_dynamic_class(finder_path=dynamic_class)
        log.info("Reader Class %s initializing" % dynamic_class)
        reader_instance = reader(settings=self.settings)
        read_data = reader_instance.read_data()
        return read_data

    def run_resolver(self, unresolved_data):
        resolved_data = dict()
        for resolver in self.dynamic_classes["resolvers"]:
            log.info("Resolver Class %s initializing" % resolver)
            resolved_data[resolver] = resolver.resolve_data(unresolved_data=unresolved_data)
        return resolved_data

    def run_writer(self, resolved_data):
        written_data = dict()
        for writer in self.dynamic_classes["readers"]:
            for write_filter in self.dynamic_classes["write_filters"]:
                log.info("Pre Write Filter Class %s initializing" % write_filter)
                resolved_data = write_filter.filter_data(resolved_data=resolved_data)
            log.info("Writer Class %s initializing" % writer)
            written_data[writer] = writer.write_data(resolved_data=resolved_data)
