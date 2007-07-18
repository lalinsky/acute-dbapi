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


def convert_connect_args(ConnectionInfo, driver, connection_method='default'): 
    """Convert ConnectionInfo config object to the appropriate arguments
    to connect for a given driver.  Connection method must be supplied if 
    this function is not familiar with the driver in use.

    Allowable connection_methods are:
      parameterized: each argument is sent as an individual parameter
      dbonly: only the database name is given as a parameter
      spaced_string: a single parm of 'dsn' is given as keyword=value pairs
      default: use the default connection argument format for this driver

    Default connection_methods are currently known for psycopg2 & pysqlite2.
    """
    #TODO: Consider using a URL instead of a class in config. 
    #TODO: See dburi.py for ideas

    if connection_method == "default":
       if driver == 'db2':
           connection_method = 'parameterized'
       elif driver == 'psycopg2':
           connection_method = 'spaced_string'
       elif driver == 'pysqlite2':
           connection_method = 'dbonly'
       else: 
           raise(Error("No connection method specified and driver is not known "
                  "to the test suite.  Can't determine how to connect!"))
    
    hostname = ConnectionInfo.hostname
    database = ConnectionInfo.database
    username = ConnectionInfo.username
    password = ConnectionInfo.password
 
    args = []
    kwargs = {}
    if connection_method == 'parameterized':
        kwargs = {
            'dsn': database,
            'uid': username,
            'pwd': password,
            }
    elif connection_method == 'dbonly':
        args = [database]
    elif connection_method == 'spaced_string':
        kwargs = {'dsn':'host=%s dbname=%s user=%s password=%s' % 
                       (hostname, database, username, password)}
    else:
        raise(Error("Unknown connection method. Can't determine how to "
                    "connect"))

    print "Connect args: %s, kwarg: %s", (args, kwargs)
    return(args, kwargs)
