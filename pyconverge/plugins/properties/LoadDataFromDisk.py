# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
import glob


class LoadDataFromDisk(ABC):
    @staticmethod
    def get_list_of_files(glob_pattern, recursive=False):
        return glob.iglob(glob_pattern, recursive=recursive)

    @abstractmethod
    def merge_contents_of_files(self, file_list):
        pass

    @abstractmethod
    def load_contents_of_files(self):
        pass
