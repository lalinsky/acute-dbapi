db_name = "kskuhlman"  #"dbapi20"

connect_kw_args = {
   'db2' : {
	'dsn': db_name, 
	'uid': 'kskuhlman',
        'user': 'kskuhlman',
	'pwd': 'kskuhlman',
   },
   'psycopg2' : {
       'dsn':
         'host=localhost dbname=%s user=kskuhlman password=kskuhlman' % db_name
   }
}

create_db_cmds = {
   'psycopg2':"psql -c 'create database %s'" % db_name,
   'db2':"db2 create database %s'" % db_name,
   'sqlite':None
}
