# -*- coding: utf-8 -*-

import os


class Helpers:

    @staticmethod
    def get_directory_tree(directory_path):
        tree = []
        for dirname, dirnames, filenames in os.walk(directory_path):
            # print path to all subdirectories first.
            for subdirname in dirnames:
                tree.append(os.path.join(dirname, subdirname))

            # print path to all filenames.
            for filename in filenames:
                tree.append(os.path.join(dirname, filename))
        return tree