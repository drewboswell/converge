# -*- coding: utf-8 -*-

import argparse


class ArgumentParser:
    @staticmethod
    def create_parser():
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

        """ HOST COMMANDS """
        # converge host --config ${config_path} ${host_name} tags
        # converge host --config ${config_path} ${host_name} applications
        group_host = argparse.ArgumentParser(add_help=False)
        group_host.add_argument("--config", action="store", required=True,
                                type=str, default=None,
                                help="path to the configuration file")
        group_host.add_argument("host_name", action="store",
                                type=str, default=None,
                                help="name of reference host")
        group_host.add_argument("init_type", action="store",
                                choices=["tags","applications"],
                                type=str, default=None,
                                help="choose information mode")

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

        sp_host = sp.add_parser("host", parents=[group_host], help="check host data")
        sp_host.set_defaults(which="host")

        # sp_run = sp.add_parser("run", parents=[group_run], help="run converge fully (check, output)")
        # sp_run.set_defaults(which="run")



        return parser
