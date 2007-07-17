""" A decorator for nose to handle tests that are expected to fail.
See the notes on the 'requires' method.  Everything else is boilerplate
& self-tests.
"""
import sys
import os
import unittest
import nose
from nose.plugins.errorclass import ErrorClass, ErrorClassPlugin

import logging
logging.basicConfig(level=logging.WARN)
log = logging.getLogger('requires')
err = sys.stderr

library_name = 'fubar'
class SupportedFeatures(object): 
    def __init__(self, library_name): 
       """ This is just a dummy.  In practice, it would set attributes
           based off of the feature set of the library.
       """ 
       self.typical_feature = True
class Library(object):
    def __init__(self, library_name):
        self.library_name = library_name
        self.supported_features = SupportedFeatures(library_name)
library = Library(library_name)


class Unsupported(Exception):
    pass
class UnsupportedError(ErrorClassPlugin):
    enabled = True
    unsupported = ErrorClass(Unsupported, label='Unsupported', 
        isfailure=False)

class UnexpectedSuccess(Exception):
    pass
class UnexpectedSuccessError(ErrorClassPlugin):
    enabled = True
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

    # Determine if the test is expected to pass
    requirements_met = True
    for req in requirements:
        if not getattr(library.supported_features, req, None):
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
                if not requirements_met:
                    raise(UnexpectedSuccess)

        newfunc = nose.tools.make_decorator(func)(newfunc)
        return newfunc
    return decorate

class TestRequires(unittest.TestCase):

    @requires('typical_feature')
    def test_success(self):
        """ Requirements met + successful test result = success """
        self.assertEqual(1, 1)

    @nose.tools.raises(AssertionError)
    @requires('typical_feature')
    def test_failure(self):
        """ Requirements met + failure result = failure """
        self.assertEqual(1, 2)

    @nose.tools.raises(UnexpectedSuccess)
    @requires('bogus_feature')
    def test_unexpected_success(self):
        """Un-met requirements + successful result = UnexpectedSuccess (failure)
        """
        self.assertEqual(1, 1)

    @nose.tools.raises(Unsupported)
    @requires('bogus_feature')
    def test_unsupported(self):
        """ Un-met requirements + failure result = Unsupported (pass) """
        self.assertEqual(1, 2)
   
    def test_skip(self):
        raise nose.plugins.skip.SkipTest

if __name__ == '__main__':
    suite = unittest.TestSuite()

    for test in [
        TestRequires,
        ]:
        suite.addTest(unittest.makeSuite(test))

    unittest.TextTestRunner(verbosity=2).run(suite)
