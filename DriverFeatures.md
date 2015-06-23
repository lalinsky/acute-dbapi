# Introduction #
Comparison of core features provided by several DB-API implementations.  Covers features that are universal to all DB-API implementations ; features that are specific to a particular driver are not covered.

| Feature | Feature Description | Default Value | pysqlite2 | MySQLdb | psycopg2 |
|:--------|:--------------------|:--------------|:----------|:--------|:---------|
| authentication  |  Database requires authentication (here for SQLite)  |  True         | False     | True    | True     |
| blob\_binary  |  BLOBs can be created from the driver's Binary type  |  True         | False     | True    | True     |
| blob\_type  |  Column definition to use for BLOBs  |  blob         | blob      | blob    | bytea    |
| call\_proc  |  Database supports stored procedures  |  True         | True      | True    | True     |
| callproc  |  Database support stored procedures (Optional)  |  True         | True      | True    | True     |
| clob\_type  |  Column definition to use for CLOBs  |  clob         | clob      | text    | text     |
| connection\_level\_exceptions  |  Exceptions are defined at the connection level (optional)  |  True         | True      | True    | True     |
| dbapi\_level  |  The DB-API level that the driver is known to support  |  2.0          | 2.0       | 2.0     | 2.0      |
| driver\_level\_datatypes  |  Available datatypes are defined at the driver level  |  True         | False     | True    | True     |
| driver\_level\_datatypes\_binary  |  The Binary datatype is defined at the driver level  |  True         | True      | True    | True     |
| explicit\_db\_create  |  Databases are created explicitly (here for SQLite)  |  True         | False     | True    | True     |
| inoperable\_closed\_connections  |  Closed connections are no longer usable  |  True         | False     | True    | True     |
| lastrowid  |  Supports lastrowid  |  True         | True      | True    | True     |
| lower\_func  |  The name of the function used to convert a string to lowercase  |  lower        | lower     | lower   | lower    |
| rollback\_defined  |  Driver defines rollback  |  True         | True      | True    | True     |
| rowcount\_reset\_empty\_fetch  |  Rowcount is reset after an empty fetch  |  True         | True      | False   | False    |
| sane\_empty\_fetch  |  Fetch should fail if no query is issued  |  True         | False     | False   | True     |
| sane\_rowcount  |  Rowcount should be set correctly by fetchmany  |  True         | False     | True    | True     |
| sane\_timestamp  |  Timestamp returns sane timestamps  |  True         | True      | False   | True     |
| scrollable\_cursors  |  Driver supports scrollable cursors  |  False        | False     | False   | False    |
| serial\_key\_def  |  Column definition to use for serial keys  |  int          | int       | int     | serial   |
| setoutputsize  |  Driver supports setoutputsize  |  True         | True      | False   | True     |
| smart\_lob\_open  |  LOBs can be read from a file handle  |  False        | False     | False   | False    |
| stored\_procedure\_language  |  Stored procedure language can be one of: Transact-SQL (Microsoft SQL Server), PL/SQL (Oracle), SQL/PL (DB2), PL/pgSQL (PostgreSQL), SQL:2003 (Anything standards compliant (MySQL))  |  SQL:2003     | SQL:2003  | SQL:2003  | PL/pgSQL  |
| time\_datatype  |  Driver supports the time datatype (optional)  |  True         | True      | True    | True     |
| time\_datatype\_subsecond  |  The time datatype supports subsecond times  |  True         | True      | True    | True     |
| time\_datatype\_time  |  The driver's time datatype supports python time values  |  True         | False     | True    | True     |
| timestamp\_datatype\_subsecond  |  The timestamp datatype supports subsecond times  |  True         | True      | False   | True     |
| transactional\_ddl  |  DDL statements are transactional (ie, need commit)  |  True         | False     | True    | True     |