# -*- coding: utf-8 -*-


"""setup.py: setuptools control."""

import re
from setuptools import setup, find_packages
import os

# try:
#     from pypandoc import convert
#
#     read_md = lambda f: convert(f, 'rst')
# except ImportError:
#    print("warning: pypandoc module not found, could not convert Markdown to RST")
try:
    from pypandoc import convert
    long_description = convert('README.md', 'rst')
    long_description = long_description.replace("\r","") # EVIL
except OSError:
    print("Pandoc not found. Long_description conversion failure.")
    import io
    # pandoc is not installed, fallback to using raw contents
    with io.open('README.md', encoding="utf-8") as f:
        long_description = f.read()


def package_files(directory):
    paths = ()
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('pyconverge/__init__.py').read(),
    re.M
).group(1)


setup(
    name="pyconverge",
    packages=["pyconverge", "tests", "pyconverge/resources", "pyconverge/schemas", *[x[0] for x in os.walk("pyconverge/plugins")]],
    entry_points={
        "console_scripts": ['converge = pyconverge.converge:main']
    },
    license='Apache License 2.0',
    version=version,
    install_requires=['pyyaml', 'pytest', 'pytest-cov', 'pykwalify'],
    description="Resolve configurations from abstract hierarchies and templates",
    long_description=long_description,
    author="Andrew Boswell",
    author_email="drewboswell@gmail.com",
    url="https://github.com/drewboswell/converge",
    platforms='any',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
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
