import pytest
import sys, os

sys.path.append(os.path.abspath(os.path.join('..', 'converge')))
import converge.converge as converge


class TestConverge:
    def test_main_arg_parser(self):
        result = converge.main()
        assert result is True
