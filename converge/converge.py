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
        if args.which == "version" and hasattr(args, "version"):
            result = converge_options.get_version_information()
            print(result)

        # init options
        elif args.which == "init" and hasattr(args, "init_type") and args.init_type == "conf":
            converge_options.init_conf(target_directory=args.path)
        elif args.which == "init" and hasattr(args, "init_type") and args.init_type == 'repository':
            converge_options.init_repository(target_directory=args.path)

        # sanity check / check config
        elif args.which == "checkconfig" and hasattr(args, "config"):
            converge_options.check_config(config_path=args.config)

        return True
    except:
        raise