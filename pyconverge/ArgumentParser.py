# -*- coding: utf-8 -*-

import argparse
import sys
import logging


class ArgumentParser:
    def __init__(self, **kwargs):
        self.configuration = kwargs.get("configuration")

    @staticmethod
    def add_sub_parser_group(sp, option_name, config):
        description = str()
        parser_group = argparse.ArgumentParser(add_help=False)
        for option in config["conf"]["default"]["args"]:
            parser_group.add_argument(option, action="store", type=str, default=None)
        options = config["modes"].keys()
        if "description" in config["conf"]["default"]:
            description = config["conf"]["default"]["description"]
        parser_group.add_argument("mode", action="store", choices=options)
        sp_new = sp.add_parser(option_name, parents=[parser_group], help=description)
        sp_new.set_defaults(which=option_name)
        return sp

    def create_parser(self):
        parser = argparse.ArgumentParser()

        # # option groups to do:
        # tag
        # host
        # application
        # property
        # hierarchy

        parser.add_argument("-v", "--verbose",
                            action="store_true", default=False, required=False,
                            help="run program in verbose/debug mode, lots of output!")
        parser.add_argument("--stdout",
                            action="store", choices=["INFO", "WARNING", "ERROR", "CRITICAL", "DEBUG"],
                            default=["WARNING"], required=False,
                            help="change stdout logging level (logs INFO to file already)")

        parser.add_argument("--config", action="store",
                            type=str, default=None,
                            help="path to the configuration file")

        group_init = argparse.ArgumentParser(add_help=False)
        group_init.add_argument("init_type", action="store",
                                choices=["repository", "conf"],
                                help="choose to initialize repository or conf")
        group_init.add_argument("path", action="store",
                                type=str, default=None,
                                help="this path will be the initialization root")

        group_checkconfig = argparse.ArgumentParser(add_help=False)
        group_checkconfig.add_argument("--config", action="store",
                                       type=str, default=None,
                                       help="path to the configuration file")

        group_run = argparse.ArgumentParser(add_help=False)
        group_run.add_argument("--config", action="store", required=True,
                               type=str, default=None,
                               help="path to the configuration file")

        group_version = argparse.ArgumentParser(add_help=False)
        group_version.add_argument("--version", action="store_true", default=True, required=False)

        # activate subparsers on main parser
        sp = parser.add_subparsers()

        sp_init = sp.add_parser("init", parents=[group_init], help="initialize configuration or repository")
        sp_init.set_defaults(which="init")

        sp_checkconfig = sp.add_parser("check", parents=[group_checkconfig],
                                       help="run sanity check on configuration")
        sp_checkconfig.set_defaults(which="check")

        sp_version = sp.add_parser("version", parents=[group_version],
                                   help="get converge version and build information")
        sp_version.set_defaults(which="version")

        """ AUTOMATIC OPTION LOADING """
        config_path = None
        for i, arg in enumerate(sys.argv):
            if arg == "--config" and len(sys.argv) > i + 1:
                config_path = sys.argv[i + 1]
                break

        if config_path:
            result = self.configuration.load_config(config_path=config_path)
            if result:
                logging.info("OK: Configuration file %s" % config_path)
                programs = self.configuration.configuration["programs"]
                for program_name, program_config in programs.items():
                    sp = self.add_sub_parser_group(sp=sp, option_name=program_name, config=program_config)

        return parser
