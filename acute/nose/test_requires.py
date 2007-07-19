""" See requires.py for documentation on the decorator & plugins. 
"""
import sys
import os
import unittest
import nose
from nose.plugins.errorclass import ErrorClass, ErrorClassPlugin
from nose.config import Config, all_config_files
from nose.plugins.manager import DefaultPluginManager 
from nose import runmodule 
#from acute.nose.requires import requires, Unimplemented, UnexpectedSuccess
from requires import (requires, Unsupported, UnexpectedSuccess,
                      UnsupportedError, UnexpectedSuccessError)

class SupportedFeatures(object): 
    typical_feature = True

supported_features = SupportedFeatures()


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

    #@nose.tools.raises(Unsupported)
    @requires('bogus_feature')
    def test_unsupported(self):
        """ Un-met requirements + failure result = Unsupported (pass) """
        self.assertEqual(1, 2)
   
    def test_skip(self):
        raise nose.plugins.skip.SkipTest

if __name__ == '__main__':
    #suite = unittest.TestSuite()

    #for test in [
    #    TestRequires,
    #    ]:
    #    suite.addTest(unittest.makeSuite(test))

    #unittest.TextTestRunner(verbosity=2).run(suite)
    runmodule(config=Config(files=all_config_files(),
                        plugins=DefaultPluginManager([UnsupportedError()]))) 

