""" Plugins and a decorator for nose.  Handles tests that are expected to fail.

    The decorator, requires, extends nose's fail status code to handle
cases where the test is expected fail based off the features supported by
the library being tested.
    If the test is expected to fail and does, then "Fail" becomes "Unsupported"
    If the test is expected to fail but instead succeeds, then "OK"
        becomes "UnexpectedSuccess."

    An example would be: Your testing a series encryption librares,
and you write a test that requires a given library to support MD5 encryption.
If the library states that it doesn't support MD5, then a test result failure
would be expected, and the status would be 'Unsupported' instead of 'Failure.'
If the test somehow succeeded, it would be an 'UnexpectedSuccess.'
"""

import sys
import os
import unittest
import nose
from nose.plugins.errorclass import ErrorClass, ErrorClassPlugin

err = sys.stderr
library_name = 'fubar'

global supported_features
supported_features = None
def set_supported_features(supported_features):
    supported_features = supported_features

class EnabledErrorClassPlugin(ErrorClassPlugin):
    """ An ErrorClassPlugin with the required stubs in place.
    Just add your error class attribute
    """
    enabled = True

    def options(self, parser, env=None):
        pass   #none needed

    def configure(self, options, conf):
        self.conf = conf


class Unsupported(Exception):
    pass
class UnsupportedError(EnabledErrorClassPlugin):
    unsupported = ErrorClass(Unsupported, label='Unsupported',
        isfailure=False)

class UnexpectedSuccess(Exception):
    pass
class UnexpectedSuccessError(ErrorClassPlugin):
    unexepected_success = ErrorClass(UnexpectedSuccess,
        label='UnexpectedSuccess', isfailure=True)

def requires(*requirements):
    """This decorator extends nose's fail status code to handle
    cases where the test is expected fail based off the features 
    supported by the library being tested.
    If the test is expected to fail and does, then "Fail" 
        becomes "Unsupported."
    If the test is expected to fail but instead succeeds, then "OK" 
        becomes "UnexpectedSuccess."

    An example would be: Your testing a series encryption librares,
    and you write a test that requires a given library to support
    MD5 encryption. If the library states that it doesn't support
    MD5, then a test result failure would be expected, and the
    status would be 'Unsupported,' instead of 'fail.'  If the test 
    somehow succeeded, it would be an 'UnexpectedSuccess.'
    """

    global required_features    
    # Determine if the test is expected to pass
    requirements_met = True
    for req in requirements:
        if not getattr(supported_features, req, None):
            requirements_met = False
            break
    
    def decorate(func):
        name = func.__name__
        def newfunc(*arg, **kw):
            exc, msg = None, None
            try:
                func(*arg, **kw)
            except:
                if requirements_met:
                    raise
                else:
                    raise(Unsupported)
            else:
                #print "requirements were", requirements_met, requirements
                #print "features are", supported_features #.getattr(requirements[0])
                if not requirements_met:
                    raise(UnexpectedSuccess)

        newfunc = nose.tools.make_decorator(func)(newfunc)
        return newfunc
    return decorate

