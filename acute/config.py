db_name = "dbapi20"
# Prefix to be used for tables
table_prefix = 'apitest_'

connect_args = {
   'db2' : {
	'dsn': db_name, 
	'uid': 'username',
	'pwd': 'password',
   },
   'psycopg2' : {
       'dsn':
         'host=localhost dbname=%s user=username  password=password ' % db_name
   }
}

create_db_cmds = {
   'psycopg2':"psql -c 'create database %s'" % db_name,
   'db2':"db2 create database %s'" % db_name,
   'sqlite':None
}
