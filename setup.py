#
# acute-dbapi setup
# Ken Kuhlman (acute at redlagoon dot net), 2007

from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages, Extension

import sys
import os

env = 'unix'
if sys.platform[:5] == 'win32': # Win32
	env = 'windows'  

setup(
    name="acute-dbapi",
    version="0.1.0",
    description="Python DB-API testsuite",
    author="Ken Kuhlman",
    author_email="acute@redlagon.net",
    license="MIT License",
    url = "http://code.google.com/p/acute-dbapi/",
    package_dir = {'':'acute'},
    long_description = """ 
acute-dbapi is::
A Python DB-API compliance test suite. It was originally derived from Stuart Bishop's DBAPI20TestSuite.

The name stands for "Anal Compliance Unit Test Environment," which is a tip-of-the-hat to Stuart, who described his testsuite in those terms.

Status::
Currently, the suite tests the compliance of a Python database driver against DB-API version 2.0 (PEP 249). It's intended to also test common implementation features that haven't found their way into the DB-API specification. 

Philosophy::
  * Extensive unit tests improve code quality, allow developers to be more courageous in making agressive changes, and improve user's ability to provide bug-feedback.
  * Sharing applicable tests between projects strengthens standards and saves time when developing new compliant modules.
  * The DB-API 2.0 standard is, like SQL '87, a "least common denominator."  In order to help drive innovation it's vital to standardize the important, popular, and necessary DBMS features in use today.  Features that haven't reached ubiquity should be made optional, not simply ignored or too lightly left as an "implemntation extension".

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
