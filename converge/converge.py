# -*- coding: utf-8 -*-

from converge.ArgumentParser import ArgumentParser
from converge.ConvergeOptions import ConvergeOptions
import time


# add main entry point
def main():
    statistics = dict()
    statistics['start_time'] = time.time()

    try:
        parser = ArgumentParser().create_parser()
        args = parser.parse_args()
    except Exception as e:
        raise

    converge_options = ConvergeOptions()
    try:
        # version option
        if hasattr(args, "which"):
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
                result = converge_options.check_config(config_path=args.config)
                if result:
                    print("OK: Configuration file %s" % args.config)
                    converge_options.check_repository()

        return True
    except:
        raise
