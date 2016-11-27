# -*- coding: utf-8 -*-


"""setup.py: setuptools control."""

import re
from glob import glob
from setuptools import setup, find_packages
import os


def package_files(directory):
    paths = ()
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('converge/__init__.py').read(),
    re.M
).group(1)

with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")

setup(
    name="pyconverge",
    packages=["converge", "resources"],
    entry_points={
        "console_scripts": ['converge = converge.converge:main']
    },
    license='Apache License 2.0',
    version=version,
    install_requires=['pyyaml','pytest','pytest-cov'],
    description="Resolve configurations from abstract hierarchies and templates",
    long_description=long_descr,
    author="Andrew Boswell",
    author_email="drewboswell@gmail.com",
    url="https://github.com/drewboswell/converge",
    platforms='any',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Financial and Insurance Industry',
        'Operating System :: OS Independent',
        'Topic :: Office/Business'
    ],
    keywords='configuration management development operations system sysadmin config converge',
    include_package_data=True,
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)
