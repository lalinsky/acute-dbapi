# The name of the db-api compliant driver to import
driver_name = "pysqlite2"
#driver_name = "psycopg2"
#driver_name = "MySQLdb"

# Prefix to be used for tables
table_prefix = 'apitest_'

class ConnectionInfo(object):
    """ Change these values to match your database & credentials """
    hostname = 'localhost'
    database = "kskuhlman"
    username = 'kskuhlman'
    password = 'itsasecret'
    port = None

