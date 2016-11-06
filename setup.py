# -*- coding: utf-8 -*-


"""setup.py: setuptools control."""

import re
from setuptools import setup, find_packages

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('converge/__init__.py').read(),
    re.M
).group(1)

with open("README.rst", "rb") as f:
    long_descr = f.read().decode("utf-8")

setup(
    name="converge",
    packages=["converge"],
    entry_points={
        "console_scripts": ['converge = converge.converge:main']
    },
    license='Apache License 2.0',
    version=version,
    install_requires=['pyyaml'],
    description="Python command line application bare bones template.",
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
        'Intended Audience :: DevOps Engineers',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: IT Operations',
        'Operating System :: OS Independent',
        'Topic :: Office/Business',
        'Topic :: Utilities :: Configuration Management',
        'Topic :: System :: Configuration Management',
        'Topic :: Software Development Configuration Management',
        'License :: OSI Approved :: Apache License 2.0',
    ],
    keywords='configuration management development operations system sysadmin config converge',
    include_package_data=True,
    package_data={
        'conf': ['converge.ini'],
        'repository': [
            'repository/applications/',
            'repository/hierarchy/',
            'repository/node_groups/',
            'repository/nodes/',
            'repository/packages/',
            'repository/templates/',
        ]
    }
)
