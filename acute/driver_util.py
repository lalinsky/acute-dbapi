#!/usr/bin/env python
import test_dbapi
import unittest
import config

class test_Psycopg(test_dbapi.DatabaseAPI20Test):
    import psycopg2
    driver = psycopg2
    connect_args = ()
    connect_kw_args = config.psycopg2_kw 
    create_db_cmd = "psql -c 'create database dbapi20_test'"
    driver_supports = test_dbapi.SupportedFeatures()

    def test_nextset(self): pass
    def test_setoutputsize(self): pass

if __name__ == '__main__':
    unittest.main()
