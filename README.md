[![Build Status](https://travis-ci.org/drewboswell/converge.svg?branch=master)](https://travis-ci.org/drewboswell/converge)
[![Coverage Status](https://coveralls.io/repos/github/drewboswell/converge/badge.svg?branch=master)](https://coveralls.io/github/drewboswell/converge?branch=master)
[![Quality Gate](https://sonarqube.com/api/badges/gate?key=drewboswell_converge)](https://sonarqube.com/dashboard/index/drewboswell_converge)
[![GitHub tag](https://img.shields.io/github/tag/drewboswell/converge.svg)]()
[![GitHub release](https://img.shields.io/github/release/drewboswell/converge.svg)]()
[![PyPI](https://img.shields.io/pypi/v/pyconverge.svg)]()
[![Py Versions](https://img.shields.io/pypi/pyversions/pyconverge.svg)](https://pypi.python.org/pypi/pyconverge/)

# converge
*Resolve Configurations from Abstract Hierarchies and Templates*

Managing configuration is hard. You sometimes need simplicity, like a few key-value properties. Sometimes you need more than a few, and you realize that a lot of your key names and values are similar and you wish you could share and reuse them. 

Wouldn't it be great to define conf in a hierarchical fashion and then have a logic engine spit out the resolved configuration? This is **converge**. Abstract hierarchies of data chewed up and spit out to simple key-values to your liking.

# How it works

# Getting started

# Examples

# A Brief History of Pain
You may have hit some (or all, like me) of these stages in the persuit of configurability:

*In short: from the file, to the GUI, back to the file you idiot.*
* Externalizing configuration from your applications, to avoid re-releases due to simple conf tuning
* Realizing that you're now managing a million de-centralized files with no similar structure
* Create or use a centralized, GUI/DB based confguration management system (woohoo! configuration liberation!)
* Realizing that automating without a middleman is both simpler and more efficient, and that you never should have used a GUI/DB. Files we always the solution, just a different kind of file, where they are in a non resolved state from which you can generate an output that meets your needs.

Files are best because:
* you can use time tested versioning systems like git or mercurial to branch, release, rollback, check history
* you can automate the modification of files with any tool you want
* doing migrations on DB values/REST endpoints sucks (because it's unecessarily complex)
