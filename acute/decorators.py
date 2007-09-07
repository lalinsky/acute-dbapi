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
from cStringIO import StringIO
#import testlib.config as config

_ops = { '<': operator.lt,
         '>': operator.gt,
         '==': operator.eq,
         '!=': operator.ne,
         '<=': operator.le,
         '>=': operator.ge,
         'in': operator.contains }

class Unsupported(Exception):
    pass
class UnexpectedSuccess(Exception):
    pass
class DidNotRaise(Exception):
    pass

global supported_features
supported_features = None
class SF(object):
    typical_feature = True
supported_features = SF()
def set_supported_features(supported_features):
    supported_features = supported_features


def requires(*requirements):
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
                    #raise(SkipTest)
                    print >> sys.stderr, "(Skipped) ",
                else:
                    print >> sys.stderr, "(Unsupported) ",
            else:
                #print ("requirements were met? %s.  They were: %s" %
                #        (requirements_met, requirements))
                #print "supported features are ::", supported_features #.getattr(requirements[0])
                if not requirements_met:
                    raise(UnexpectedSuccess)

        newfunc.__name__ = name
        newfunc.__doc__ = doc
        return newfunc
    return decorate



def sa_unsupported(*dbs):
    """Mark a test as unsupported by one or more database implementations"""
    
    def decorate(fn):
        fn_name = fn.__name__
        def maybe(*args, **kw):
            if config.db.name in dbs:
                print "'%s' unsupported on DB implementation '%s'" % (
                    fn_name, config.db.name)
                return True
            else:
                return fn(*args, **kw)
        try:
            maybe.__name__ = fn_name
        except:
            pass
        return maybe
    return decorate

def sa_supported(*dbs):
    """Mark a test as supported by one or more database implementations"""
    
    def decorate(fn):
        fn_name = fn.__name__
        def maybe(*args, **kw):
            if config.db.name in dbs:
                return fn(*args, **kw)
            else:
                print "'%s' unsupported on DB implementation '%s'" % (
                    fn_name, config.db.name)
                return True
        try:
            maybe.__name__ = fn_name
        except:
            pass
        return maybe
    return decorate

def sa_exclude(db, op, spec):
    """Mark a test as unsupported by specific database server versions.

    Stackable, both with other excludes and supported/unsupported. Examples::
      # Not supported by mydb versions less than 1, 0
      @exclude('mydb', '<', (1,0))
      # Other operators work too
      @exclude('bigdb', '==', (9,0,9))
      @exclude('yikesdb', 'in', ((0, 3, 'alpha2'), (0, 3, 'alpha3')))
    """

    def decorate(fn):
        fn_name = fn.__name__
        def maybe(*args, **kw):
            if config.db.name != db:
                return fn(*args, **kw)

            have = config.db.dialect.server_version_info(
                config.db.contextual_connect())

            oper = hasattr(op, '__call__') and op or _ops[op]

            if oper(have, spec):
                print "'%s' unsupported on DB %s version '%s'" % (
                    fn_name, config.db.name, have)
                return True
            else:
                return fn(*args, **kw)
        try:
            maybe.__name__ = fn_name
        except:
            pass
        return maybe
    return decorate

def raises(exception):
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

    #TODO: Was relying on nose.tools.raises
    #@nose.tools.raises(UnexpectedSuccess)
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
   
    #def test_skip(self):
    #    raise nose.plugins.skip.SkipTest

if __name__ == "__main__":
    class SupportedFeatures(object): 
        def __init__(self, library_name): 
            """ This class should contain attributes describing the
            feature set of the library.
            """ 
            self.typical_feature = True
    library_name = 'junk'
    library_features = SupportedFeatures(library_name)
    set_supported_features(supported_features=library_features)


    suite = unittest.TestSuite()

    for test in [TestRequires]:
        suite.addTest(unittest.makeSuite(test))

    unittest.TextTestRunner(verbosity=2).run(suite)

