[![GitHub tag](https://img.shields.io/github/tag/drewboswell/converge.svg)]()
[![GitHub release](https://img.shields.io/github/release/drewboswell/converge.svg)]()
[![PyPI](https://img.shields.io/pypi/v/pyconverge.svg)](https://pypi.python.org/pypi/pyconverge/)
[![Py Versions](https://img.shields.io/pypi/pyversions/pyconverge.svg)](https://pypi.python.org/pypi/pyconverge/)

[![Build Status](https://travis-ci.org/drewboswell/converge.svg?branch=master)](https://travis-ci.org/drewboswell/converge)
[![Coverage Status](https://coveralls.io/repos/github/drewboswell/converge/badge.svg?branch=master)](https://coveralls.io/github/drewboswell/converge?branch=master)
[![Quality Gate](https://sonarqube.com/api/badges/gate?key=drewboswell_converge)](https://sonarqube.com/dashboard/index/drewboswell_converge)
[![Code Smells](https://sonarqube.com/api/badges/measure?key=drewboswell_converge&metric=code_smells)](https://sonarqube.com/dashboard/index/drewboswell_converge)
[![File Complexity](https://sonarqube.com/api/badges/measure?key=drewboswell_converge&metric=file_complexity)](https://sonarqube.com/dashboard/index/drewboswell_converge)
[![Vulnerabilities](https://sonarqube.com/api/badges/measure?key=drewboswell_converge&metric=vulnerabilities)](https://sonarqube.com/dashboard/index/drewboswell_converge)
[![Technical Dept](https://sonarqube.com/api/badges/measure?key=drewboswell_converge&metric=sqale_debt_ratio)](https://sonarqube.com/dashboard/index/drewboswell_converge)
[![Lines of code](https://sonarqube.com/api/badges/measure?key=drewboswell_converge&metric=ncloc)](https://sonarqube.com/dashboard/index/drewboswell_converge)


# converge
*Resolve Data from Abstract Hierarchies and Templates*

Managing configuration is hard. More often than not you have high key/values duplication and storage. [DRY](https://en.wikipedia.org/wiki/Don't_repeat_yourself) your tears, it's time for some hierarchical magic, so you can get back to the important stuff.

This is where **converge** comes in. There are a few basic concepts when using or extend converge: 
* Readers: get data from your backends
* Filters: filter data before or after resolution (*example: search & replace values, inject data post resolution*)
* Resolvers: convert abstract data to resolved data
* Writers: output your data to the format and backend you need

Abstract hierarchies of data chewed up and spit out to your liking.

# Getting started
install pyconverge, this will add the `converge` command to your classpath using setup.py/PyPi
```bash
pip install pyconverge
converge version
converge --help
```

Create a converge.yaml.template file in your project working directory, modify and move it to converge.yaml 
```bash
# create the converge.yaml.template file
converge init conf
# modify your converge parameters
vim converge.yaml.template
# activate converge
mv converge.yaml.template converge.yaml
# verify the integrity of your configuration file
converge check
```

Try it out! You chould have a bunch more options!
```bash
converge --help
```

# Example: Simple testing
create a converge.yaml as described above
```bash
converge init conf
mv converge.yaml.template converge.yaml
converge check
```
Create a sample repository structure
```bash
converge init repository target_directory

# you should now have the following structure
find target_directory/ -type d
# this is where the application centric data goes
./data
./data/default
./data/default/shared
./data/default/app
# the hierarchy file is situated here
./hierarchy
# target (or host for most) centric data resides here
./targets
./targets/hosts
./targets/mapping
```

# Configuration: converge.yaml
This file is a bit peculiar, it allows you to add programs, options, configurations on the fly. Let's try it out
before adding the converge.yaml:
```bash
converge --help
# positional arguments:
#  {init,check,version}
#    init                initialize configuration or repository
#    check               run sanity check on configuration
#    version             get converge version and build information
```

put the following in a converge.yaml:
```yaml
conf:
    default:
        logging_level: "INFO"
programs:
    # user command
    amazingcommand:
        # arguments expected by the command
        args:
            - "argument_one"
            - "argument_two"
        # description for the python help
        description: "application description"
        modes:
            amazing_mode_one:
                - "com.insane.class.path.Class1"
                - "com.insane.class.path.Class2"
            amazing_mode_two:
                - "com.insane.class.path.Class1"
                - "com.insane.class.path.Class3"
```

Now you should see a new option:
```bash
converge --help
# positional arguments:
#  {init,check,version,amazingcommand}
#    init                initialize configuration or repository
#    check               run sanity check on configuration
#    version             get converge version and build information
#    amazingcommand      application description <-- MAGIC STUFF with description!!
```

And even more so there are sub-options available too:
```bash
converge amazingcommand --help
# usage: converge-runner.py amazingcommand [-h]
#                                         argument_one argument_two
#                                         {amazing_mode_two,amazing_mode_one}
#
# positional arguments:
#  argument_one
#  argument_two
#  {amazing_mode_two,amazing_mode_one}

```

# Example: Configuration for Java property files

# A rough overview

A general example in diagram form:

![Alt text](docs/converge-diagram.png "Converge Overview")

# A Brief History of Pain
You may have hit some (or all) of these stages in the pursuit of configurability:

*In short: from the file, to the GUI, back to the file you idiot.* #wevecomefullcircle
* Externalize configuration from your applications, to avoid re-releases due to simple conf tuning
* Realizing that you're now managing a million de-centralized files with no similar structure
* Create or use a centralized, GUI/DB based configuration management system (woohoo! configuration liberation!)
* Realizing that you are missing flexibility, automation is complex, added abstraction layers are painful. 

The better model is to accept any data format, process it and output it as you wish.

Files are better because:
* you can use time tested versioning systems like git or mercurial to branch, release, rollback, check history
* you can automate the modification of files with any tool you want
* doing migrations/deployment/modifications on DB values/REST endpoints sucks (unnecessarily complex)
