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
    long_description = """ 
acute-dbapi is::
A Python DB-API compliance test suite. It was originally derived from Stuart Bishop's DBAPI20TestSuite.

The name stands for "Anal Compliance Unit Test Environment," which is a tip-of-the-hat to Stuart, who described his testsuite in those terms.

SVN version::
 <http:/http://acute-dbapi.googlecode.com/svn/trunk/>
""",
    classifiers = [
         "Development Status :: 4 - Beta",
         "Intended Audience :: Developers",
         "License :: OSI Approved :: MIT License",
         "Programming Language :: Python",
         "Topic :: Database :: Front-Ends",
     ]
     )

