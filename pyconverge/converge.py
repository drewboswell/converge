# -*- coding: utf-8 -*-

from pyconverge.ArgumentParser import ArgumentParser
from pyconverge.ConfigValidator import ConfigValidator
from .BaseClassLoader import BaseClassLoader
import time
import logging
import sys
logging.getLogger("pykwalify.core").setLevel(logging.WARN)


# add main entry point
def main():
    statistics = dict()
    statistics['start_time'] = time.time()

    configuration = ConfigValidator()

    try:
        parser = ArgumentParser(config_validator=configuration).create_parser()
        args = parser.parse_args()
    except Exception as e:
        raise

    try:
        # version option
        if hasattr(args, "which"):
            if args.which == "version" and hasattr(args, "version"):
                statistics['opt_version'] = time.time()
                result = configuration.get_version_information()
                print(result)
                statistics['opt_version'] = time.time() - statistics['opt_version']

            # init options
            elif args.which == "init" and hasattr(args, "init_type") and args.init_type == "conf":
                statistics['opt_init_conf'] = time.time()
                configuration.init_conf(target_directory=args.path)
                statistics['opt_init_conf'] = time.time() - statistics['opt_init_conf']
            elif args.which == "init" and hasattr(args, "init_type") and args.init_type == 'repository':
                statistics['opt_init_repo'] = time.time()
                configuration.init_repository(target_directory=args.path)
                statistics['opt_init_repo'] = time.time() - statistics['opt_init_repo']

            # sanity check / check config
            elif args.which == "check" and hasattr(args, "config"):
                statistics['opt_check'] = time.time()
                result = configuration.check_config(config_path=args.config)
                if result:
                    # todo: add validator parsing from yaml file loaded above (dynamic checks)
                    logging.info("OK: Configuration file %s" % args.config)
                statistics['opt_check'] = time.time() - statistics['opt_check']
            elif args.which and hasattr(args, "config"):
                statistics[args.which] = time.time()
                settings = configuration.configuration
                mode = args.mode
                class_loader = BaseClassLoader(settings=settings)
                class_loader.run_instruction_set(program=args.which, mode=mode, settings=settings, arguments=args)
                statistics[args.which] = time.time() - statistics[args.which]
            else:
                print("Application exited prematurely, options passed without error but nothing happened!")
                sys.exit(1)
        # statistics calculations
        statistics["end_time"] = time.time()
        statistics["total_time"] = statistics["end_time"] - statistics['start_time']
        logging.info(statistics)
        logging.info("Time elapsed: %f" % statistics["total_time"])
        return True
    except:
        # statistics calculations
        statistics["end_time"] = time.time()
        statistics["total_time"] = statistics["end_time"] - statistics['start_time']

        logging.info("Time elapsed: %f" % statistics["total_time"])
        raise