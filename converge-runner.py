#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-


"""Convenience wrapper for running converge directly from source tree."""

from pyconverge.converge import main
from pyconverge.plugins.properties.PropertiesPlugin import main as mainer

if __name__ == '__main__':
    # main()
    mainer()
