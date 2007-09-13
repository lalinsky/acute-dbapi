""" Utility functions for the acute DBAPI testsuite """

def import_module(driver_name):
    """ Import a database module by name.  SQLite requires special handling.
    There may be others.. if so, please add them here!
    """
    if driver_name not in ['sqlite3', 'pysqlite2']:
        driver_module = __import__(driver_name)
    else:
        try:
            # SQLite is only included in python 2.5 & above. Previously
            # it was external & named "pysqlite2"
            from sqlite3 import dbapi2 as driver_module
        except ImportError:
            from pysqlite2 import dbapi2 as driver_module
    return driver_module


