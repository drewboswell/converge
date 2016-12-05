import pytest
import sys, os

sys.path.append(os.path.abspath(os.path.join('..', 'converge')))
from converge import converge as converge
import converge.__main__ as mainexec


class TestConverge:
    def test_main_arg_parser(self):
        argument_to_test = "version"
        sys.argv.append(argument_to_test)
        result = converge.main()
        sys.argv.remove(argument_to_test)
        assert result is True

    def test_main_arg_parser_bad_argument(self):
        argument_to_test = "break arguments"
        sys.argv.append(argument_to_test)
        result = converge.main()
        sys.argv.remove(argument_to_test)
        assert result is False

    def test_package_executable_main(self):
        argument_to_test = "version"
        sys.argv.append(argument_to_test)
        result = mainexec.main()
        sys.argv.remove(argument_to_test)
        assert result is True

    def test_arg_parser_version(self):
        argument_to_test = "version"
        sys.argv.append(argument_to_test)
        result = converge.main()
        sys.argv.remove(argument_to_test)
        assert result is True

    def test_arg_parser_init_configuration_file(self):
        arguments_to_test = ["init",
                             "conf",
                             '%s/%s' % ("generated_by_tests", "test_arg_parser_init_configuration_file")]
        sys.argv.extend(arguments_to_test)
        result = converge.main()
        [sys.argv.remove(x) for x in arguments_to_test]
        assert result is True