# The name of the db-api compliant driver to import
driver_name = "pysqlite2"
#driver_name = "psycopg2"

# What format does the driver expect it's connection arguments in?
# Allowable values are: 
#   parameterized: each argument is sent as an individual parameter
#   dbonly: only the database name is given as a parameter
#   spaced_string: a single parm of 'dsn' is given as keyword=value pairs
#   default: use the default connection argument format for this driver
#            Default formats are currently known for psycopg2 & pysqlite2
connection_method = 'parameterized'

# The name of the database to connect to
db_name = "kskuhlman" #"dbapi20"

# Prefix to be used for tables
table_prefix = 'apitest_'

class ConnectionInfo(object):
    """ Change these values to match your database & credentials """
    hostname = 'localhost'
    database = db_name
    username = 'kskuhlman'
    password = 'itsasecret'
    
# Database creation commands per database supported by this test suite.
create_db_cmds = {
   'psycopg2' : "psql -c 'create database %s'" % db_name,
   'db2' : "db2 create database %s'" % db_name,
   'pysqlite2' : None
}
