# The name of the db-api compliant driver to import
driver_name = "pysqlite2"
#driver_name = "psycopg2"
#driver_name = "MySQLdb"

# Set DBMS to an appropriate value if using a driver that knows
# how to connect to multiple backends (eg, ODBC).
#  There needs to be a matching database by this name in databases.py

##dbms = 'oracle'

# Prefix to be used for tables
table_prefix = 'apitest_'

class ConnectionInfo(object):
    """ Change these values to match your database & credentials """
    hostname = 'localhost'
    database = "kskuhlman"
    username = 'kskuhlman'
    password = 'itsasecret'
    port = None

