[![GitHub tag](https://img.shields.io/github/tag/drewboswell/converge.svg)]()
[![GitHub release](https://img.shields.io/github/release/drewboswell/converge.svg)]()
[![PyPI](https://img.shields.io/pypi/v/pyconverge.svg)](https://pypi.python.org/pypi/pyconverge/)
[![Py Versions](https://img.shields.io/pypi/pyversions/pyconverge.svg)](https://pypi.python.org/pypi/pyconverge/)

[![Build Status](https://travis-ci.org/drewboswell/converge.svg?branch=master)](https://travis-ci.org/drewboswell/converge)
[![Coverage Status](https://coveralls.io/repos/github/drewboswell/converge/badge.svg?branch=master)](https://coveralls.io/github/drewboswell/converge?branch=master)
[![Quality Gate](https://sonarqube.com/api/badges/gate?key=drewboswell_converge)](https://sonarqube.com/dashboard/index/drewboswell_converge)
[![Code Smells](https://sonarqube.com/api/badges/measure?key=drewboswell_converge&metric=code_smells)](https://sonarqube.com/dashboard/index/drewboswell_converge)
[![Function Complexity](https://sonarqube.com/api/badges/measure?key=drewboswell_converge&metric=function_complexity)](https://sonarqube.com/dashboard/index/drewboswell_converge)
[![Vulnerabilities](https://sonarqube.com/api/badges/measure?key=drewboswell_converge&metric=vulnerabilities)](https://sonarqube.com/dashboard/index/drewboswell_converge)
[![Technical Dept](https://sonarqube.com/api/badges/measure?key=drewboswell_converge&metric=sqale_debt_ratio)](https://sonarqube.com/dashboard/index/drewboswell_converge)
[![Lines of code](https://sonarqube.com/api/badges/measure?key=drewboswell_converge&metric=ncloc)](https://sonarqube.com/dashboard/index/drewboswell_converge)



# converge
*Resolve Data from Abstract Hierarchies and Templates*

Managing configuration is hard. Sometimes you need simplicity, like a few key-value properties. Sometimes you realize that a lot of your data is similar and you wish you could apply abstraction to share and reuse them. 

This is where **converge** comes in. Choose your logic engines: 
* Readers: get data from your backends
* Pre-Filters: filter data before resolution
* Resolvers: convert abstract data to resolved data
* Post-Filters: filter resolved data (*example: search & replace values, inject data post resolution*)
* Writers: output your data to the format and backend of your choice

Abstract hierarchies of data chewed up and spit out to your liking.

# How it works

![Alt text](docs/converge-diagram.png "Converge Overview")

# Getting started

# Examples

# A Brief History of Pain
You may have hit some (or all) of these stages in the pursuit of configurability:

*In short: from the file, to the GUI, back to the file you idiot.*
* Externalize configuration from your applications, to avoid re-releases due to simple conf tuning
* Realizing that you're now managing a million de-centralized files with no similar structure
* Create or use a centralized, GUI/DB based configuration management system (woohoo! configuration liberation!)
* Realizing that you are missing flexibility, automation is complex, added abstraction layers are painful. 

The better model is to accept any data format, process it and output it as you wish.

Files are better because:
* you can use time tested versioning systems like git or mercurial to branch, release, rollback, check history
* you can automate the modification of files with any tool you want
* doing migrations on DB values/REST endpoints sucks (unnecessarily complex)
