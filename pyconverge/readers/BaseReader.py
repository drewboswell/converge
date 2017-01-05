from abc import ABC, abstractmethod


class BaseReader(ABC):

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
