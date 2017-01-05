from abc import ABC, abstractmethod


class BaseWriter(ABC):

    @abstractmethod
    def write_data(self, resolved_data):
        pass
