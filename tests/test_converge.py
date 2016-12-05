import pytest
import sys, os

sys.path.append(os.path.abspath(os.path.join('..', 'converge')))
from converge import converge as converge
import converge.__main__ as mainexec

class TestConverge:
    def test_main_arg_parser(self):
        result = converge.main()
        assert result is True

    def test_main_arg_parser_bad_argument(self):
        sys.argv.append("break arguments")
        result = converge.main()
        sys.argv.remove("break arguments")
        assert result is False

    def test_package_executable_main(self):
        result = mainexec.main()
        assert result is True