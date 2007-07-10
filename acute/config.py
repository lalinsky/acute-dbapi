# The name of the db-api compliant driver to import
db_driver = "pysqlite2"

# The name of the database to connect to
db_name = "dbapi20"

# Prefix to be used for tables
table_prefix = 'apitest_'

# Connection arguments per database supported by this testsuite.
connect_args = {
   'db2' : {
	'dsn': db_name, 
	'uid': 'username',
	'pwd': 'password',
   },
   'psycopg2' : {
       'dsn':
         'host=localhost dbname=%s user=username  password=password ' % db_name
   },
   'pysqlite2': (db_name,)
}

# Database creation commands per database supported by this test suite.
create_db_cmds = {
   'psycopg2' : "psql -c 'create database %s'" % db_name,
   'db2' : "db2 create database %s'" % db_name,
   'pysqlite2' : None
}
