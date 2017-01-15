# -*- coding: utf-8 -*-

from pyconverge.ArgumentParser import ArgumentParser
from pyconverge.ConfigValidator import ConfigValidator
from .BaseClassLoader import BaseClassLoader
import time
import logging
logging.getLogger("pykwalify.core").setLevel(logging.WARN)


# add main entry point
def main():
    statistics = dict()
    statistics['start_time'] = time.time()

    try:
        parser = ArgumentParser().create_parser()
        args = parser.parse_args()
    except Exception as e:
        raise

    configuration = ConfigValidator()
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
                    logging.info("OK: Configuration file %s" % args.config)
                    configuration.check_repository()
                statistics['opt_check'] = time.time() - statistics['opt_check']

            # run converge fully
            elif args.which == "run" and hasattr(args, "config"):
                statistics['opt_run'] = time.time()
                # result = configuration.check_config(config_path=args.config)
                # if result:
                #     class_loader = BaseClassLoader(settings=configuration.paths)
                #     class_loader.run_plugins(**configuration.paths)
                settings_yaml = """
default:
  logging_level: "INFO"
programs:
  properties:
    conf:
      yaml:
        base_dir: "pyconverge/resources/repository"
        schema_path: "schemas"
        hierarchy_path: "hierarchy/hierarchy.yaml"
      properties:
        base_dir: "pyconverge/resources"
        hierarchy_path: "hierarchy.yaml"
        host_glob: "targets/hosts/**/*.yaml"
        mapping_glob: "targets/mapping/**/*.yaml"
        dependency_glob: "data/**/dependencies.properties"
        properties_glob: "data/**/*.properties"
        output_dir: "output"
    instructions:
      - validate:
        - "pyconverge.plugins.yaml.Hierarchy.Validator"
        - "pyconverge.plugins.yaml.Targets.Validator"
      - read_hierarchy:
        - "pyconverge.plugins.yaml.Hierarchy.Hierarchy"
      - read_data:
        - "pyconverge.plugins.properties.PropertiesFinder.PropertiesFinder":
          filter:
            - "pyconverge.plugins.properties.PropertiesFilters.ReadFilter"
      - resolve:
        - "pyconverge.plugins.properties.PropertiesResolver.PropertiesResolver"
      - write:
        - "pyconverge.plugins.properties.PropertiesWriter.PropertiesWriter":
          filter:
            - "pyconverge.plugins.placeholder.PlaceholderFilters.PlaceholderFilter"
                """
                
                import yaml
                settings = yaml.load(settings_yaml)
                class_loader = BaseClassLoader(settings=settings)
                # print(settings)
                class_loader.run_instruction_set(program="properties")
                # class_loader.run_plugins(**configuration.paths)
                statistics['opt_run'] = time.time() - statistics['opt_run']

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