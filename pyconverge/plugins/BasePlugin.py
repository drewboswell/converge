# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod


class BasePlugin(ABC):

    def read_data(self):
        result = dict()
        result["hierarchy"] = self.read_hierarchy
        result["targets"] = self.read_targets
        result["repository"] = self.read_repository
        return result

    @abstractmethod
    def read_hierarchy(self):
        pass

    @abstractmethod
    def read_targets(self):
        pass

    @abstractmethod
    def read_repository(self):
        pass

    @abstractmethod
    def resolve_all_data(self, periodic_write=False):
        pass

    @abstractmethod
    def resolve_target_data(self, target, periodic_write=False):
        pass

    @abstractmethod
    def write_data(self, resolved_data):
        pass
