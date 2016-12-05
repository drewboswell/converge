# -*- coding: utf-8 -*-

import argparse
import os
import pkg_resources
from shutil import copyfile
from .__init__ import __version__, __source_repository__, __release_repository__


# add main entry point
def main():
    try:
        parser = argparse.ArgumentParser()
        # options to add are the following:
        # init
        # checkconfig
        # diff
        # run

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
        group_checkconfig.add_argument("--sanitycheck", action="store_true", default=True, required=False)

        group_diff = argparse.ArgumentParser(add_help=False)
        group_diff.add_argument("--diff", action="store_true", default=True, required=False)

        group_run = argparse.ArgumentParser(add_help=False)
        group_run.add_argument("--run", action="store_true", default=True, required=False)

        group_version = argparse.ArgumentParser(add_help=False)
        group_version.add_argument("--version", action="store_true", default=True, required=False)

        sp = parser.add_subparsers()
        sp_init = sp.add_parser("init", parents=[group_init], help="initialize configuration or repository")
        sp_checkconfig = sp.add_parser("checkconfig", parents=[group_checkconfig],
                                       help="run sanity check on configuration")
        sp_diff = sp.add_parser("diff", parents=[group_diff],
                                help="run converge and compare to previous version without committing changes to output")
        sp_run = sp.add_parser("run", parents=[group_run], help="run converge fully (check, output)")
        sp_version = sp.add_parser("version", parents=[group_version],
                                   help="get converge version and build information")

        args = parser.parse_args()
        try:
            if hasattr(args, "version"):
                version_information = """
                Application Converge
                Version: {version_number:s}
                Project Source: {source_repository:s}
                Release repository: {release_repository:s}
                """
                version_arguments = {
                    "version_number": __version__,
                    "source_repository": __source_repository__,
                    "release_repository": __release_repository__
                }
                print(version_information.format(**version_arguments))
                return True

            elif hasattr(args, "init_type"):
                init_type = args.init_type
                full_path = os.path.join(os.getcwd(), args.path)
                init_path = os.path.isdir(full_path)
                if init_path:
                    if init_type == 'conf':
                        print("will create configuration file in %s/converge.ini.template" % full_path)
                        resource_package = __name__
                        resource_path = '/'.join(('resources', 'etc/converge.ini.template'))
                        template = pkg_resources.resource_filename(resource_package, resource_path)
                        print("Copying template from %s to %s" % (template, full_path))
                        copyfile(template, os.path.join(full_path, "converge.ini.template"))
                        print("New configuration can be found in: %s" % full_path)
                        return os.path.isfile(os.path.join(full_path, "converge.ini.template"))
                else:
                    print("Directory does not exist: %s" % full_path)
        except:
            raise

    except:
        return False

    return True
