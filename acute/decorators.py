""" A requires decorator for unittest. Handles tests that are expected to fail.

    The decorator, requires, modifies a test's result status to handle
cases where the test is expected fail (according to the features supported by
the library being tested).
    If the test is expected to fail and does, then "Fail" becomes "Unsupported"
    If the test is expected to fail but instead succeeds, then "OK"
        becomes "UnexpectedSuccess."

    An example would be: Your testing a series encryption librares,
and you write a test that requires a given library to support MD5 encryption.
If the library states that it doesn't support MD5, then a test result failure
would be expected, and the status would be 'Unsupported' instead of 'Failure.'
If the test somehow succeeded, it would be an 'UnexpectedSuccess.'
"""

import unittest, re, sys, os, operator

class Unsupported(Exception):
    pass
class UnexpectedSuccess(Exception):
    pass
class DidNotRaise(Exception):
    pass


# A dummpy class that will get over-writing in real usage.
class SF(object):
    typical_feature = True
supported_features = SF()
def set_supported_features(supported_features):
    supported_features = supported_features


def requires(*requirements):
    "Declare a test as requiring a feature or list of features in order to succeed."
    global required_features
    # Determine if the test is expected to pass
    requirements_met = True
    #print ("requires requirements: %s.  Supported: %s" % 
    #           (requirements, supported_features))
    for req in requirements:
        if not getattr(supported_features, req, None):
            requirements_met = False
            break

    def decorate(func):
        name = func.__name__
        doc = func.__doc__
        def newfunc(*arg, **kw):
            exc, msg = None, None
            try:
                func(*arg, **kw)
            except:
                if requirements_met:
                    raise
                elif 'amiracle' in requirements:
                    print >> sys.stderr, "(Skipped) ",
                else:
                    print >> sys.stderr, "(Unsupported) ",
            else:
                if not requirements_met and not 'amiracle' in requirements:
                    raise(UnexpectedSuccess)

        newfunc.__name__ = name
        newfunc.__doc__ = doc
        return newfunc
    return decorate


def raises(exception):
    "Declare that a test will raise a particular error."
    def decorate(func):
        name = func.__name__
        doc = func.__doc__
        def newfunc(*arg, **kw):
            try:
                func(*arg, **kw)
            except exception:
                return True
            else:
                return DidNotRaise
        newfunc.__name__ = name
        newfunc.__doc__ = doc
        return newfunc
    return decorate
            
                 

class TestRequires(unittest.TestCase):

    @requires('typical_feature')
    def test_success(self):
        """ Requirements met + successful test result = success """
        self.assertEqual(1, 1)

    @raises(AssertionError)
    @requires('typical_feature')
    def test_failure(self):
        """ Requirements met + failure result = failure """
        self.assertEqual(1, 2)

    @raises(UnexpectedSuccess)
    @requires('bogus_feature')
    def test_unexpected_success(self):
        """Un-met requirements + successful result = UnexpectedSuccess (failure)
        """
        self.assertEqual(1, 1)

    @raises(Unsupported)
    @requires('bogus_feature')
    def test_unsupported(self):
        """ Un-met requirements + failure result = Unsupported (pass) """
        # This test makes sure that the right error is raised
        self.assertEqual(1, 2)

    @requires('bogus_feature')
    def test_unsupported2(self):
        """ Un-met requirements + failure result = Unsupported (pass) Test 2"""
        # This test makes sure that the error is not handled as a failure.
        self.assertEqual(1, 2)
   

if __name__ == "__main__":

    suite = unittest.TestSuite()

    for test in [TestRequires]:
        suite.addTest(unittest.makeSuite(test))

    unittest.TextTestRunner(verbosity=3).run(suite)

