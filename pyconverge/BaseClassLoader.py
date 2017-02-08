# -*- coding: utf-8 -*-

from importlib import import_module
import logging

log = logging.getLogger(__name__)


# Dynamically import libraries based on user preferences
def get_dynamic_class(finder_path):
    module_name, class_name = finder_path.rsplit('.', 1)
    module = import_module(module_name)
    log.debug("Imported Module %s, Class %s" % (module_name, class_name))
    return getattr(module, class_name)


class ConvergeData(object):
    data = dict()
    targets = dict()


class BaseClassLoader:
    def __init__(self, settings):
        self.programs = settings["programs"]
        self.settings = dict()
        self.instructions = list()

    def run_instruction_set(self, **kwargs):
        result = False
        data = ConvergeData()
        program_name = kwargs.get("program")
        mode = kwargs.get("mode")
        arguments = kwargs.get("arguments")
        settings = kwargs.get("settings")

        self.instructions = self.programs[program_name]["modes"][mode]
        self.settings = self.programs[program_name]["conf"]

        for instruction in self.instructions:
            dynamic_class_path = instruction
            runner_class = get_dynamic_class(finder_path=dynamic_class_path)
            runner = runner_class()

            data = runner.run(data=data, conf=settings, **arguments)
        return result
