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
from requires import (requires, Unsupported, UnexpectedSuccess,
                      UnsupportedError, UnexpectedSuccessError)


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
        # This test makes sure that the right error is raised
        self.assertEqual(1, 2)

    @requires('bogus_feature')
    def test_unsupported2(self):
        """ Un-met requirements + failure result = Unsupported (pass) Test 2"""
        # This test makes sure that the error is not handled as a failure.
        self.assertEqual(1, 2)
   
    def test_skip(self):
        raise nose.plugins.skip.SkipTest

if __name__ == '__main__':

    class SupportedFeatures(object): 
        def __init__(self, library_name): 
            """ This class should contain attributes describing the
            feature set of the library.
            """ 
            self.typical_feature = True
    library_features = SupportedFeatures(library_name)
    set_supported_features(supported_features=library_features)

    runmodule(config=Config(files=all_config_files(),
              plugins=DefaultPluginManager(
                         [UnsupportedError(), UnexpectedSuccessError()])))
