from abc import ABC, abstractmethod


class BaseResolver(ABC):

    @abstractmethod
    def resolve_data(self, unresolved_data):
        pass
