# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
import glob


class LoadDataFromDisk(ABC):
    @staticmethod
    def get_list_of_files(glob_pattern, recursive=False):
        return glob.glob(glob_pattern, recursive=recursive)

    @abstractmethod
    def merge_contents_of_files(self, file_list):
        pass

    @abstractmethod
    def read_data(self):
        pass
