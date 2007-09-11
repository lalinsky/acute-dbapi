#
# acute-dbapi setup
# Ken Kuhlman (acute at redlagoon dot net), 2007

from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages, Extension

import sys
import os

setup(
    name="acute-dbapi",
    version="0.1.0",
    description="Python DB-API testsuite",
    author="Ken Kuhlman",
    author_email="acute@redlagon.net",
    license="MIT License",
    url = "http://code.google.com/p/acute-dbapi/",
    ##py_modules=[ 'acute' ],
    #install_requires=['nose>=0.10a1',],
    #extras_requires={
    #    'core-testing':["pysqlite", ]
    #},
    packages = ['acute'],
    package_dir = {'acute':'acute'},

    #test_suite = 'nose.collector',

    #TODO: This is also the project summary page on google code. Keep in sync.
    long_description = """ 
Welcome to the home page for acute-dbapi, a DB-API compliance test suite.  Acute is still in it's infancy, but it's reached the level of maturity that it would benefit from community input.  It currently contains 71 tests, and many more will be added soon.

Comments, suggestions, and patches are all warmly welcome.  There are several TODOs listed in the [TODO] file, and many more generously sprinkled throughout the code; if you'd like to help out but don't know where to begin, feel free to take a crack at one of them!

Please read the project's [README] for an introduction to the suite.  You'll also find usage, architecture, and project philosophy information there.

If you just want to see the results, take a look at TestResults, and DriverFeatures on the project wiki.
""",
    classifiers = [
         "Development Status :: 4 - Beta",
         "Intended Audience :: Developers",
         "License :: OSI Approved :: MIT License",
         "Programming Language :: Python",
         "Topic :: Database :: Front-Ends",
     ]
     )

