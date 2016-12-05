# -*- coding: utf-8 -*-

from converge.ArgumentParser import ArgumentParser
from converge.ConvergeOptions import ConvergeOptions


# add main entry point
def main():

    try:
        parser = ArgumentParser().create_parser()
        args = parser.parse_args()
    except Exception as e:
        raise

    converge_options = ConvergeOptions()
    try:
        # version option
        if hasattr(args, "version"):
            result = converge_options.get_version_information()
            print(result)

        # init options
        elif hasattr(args, "init_type") and args.init_type == "conf":
            converge_options.init_conf(args.path)
        elif hasattr(args, "init_type") and args.init_type == 'repository':
            converge_options.init_repository(args.path)

        return True
    except:
        raise