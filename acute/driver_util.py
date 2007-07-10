#!/usr/bin/env python
import test_dbapi
import unittest
import config

db_driver = "psycopg2"
driver_module = __import__(db_driver)

class test_db_driver(test_dbapi.DBAPITest):
    driver = driver_module
    connect_kw_args = config.connect_kw_args[db_driver]
    create_db_cmd = config.create_db_cmds[db_driver]
    driver_supports = test_dbapi.SupportedFeatures()

    def test_nextset(self): pass
    def test_setoutputsize(self): pass

if __name__ == '__main__':
    unittest.main()
