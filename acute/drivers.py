#!/usr/bin/env python

# See the README for details on how this module works (if it's not obvious).

# NOTES: 
# When subclassing DriverBase, be sure to match the name of the driver 
#    that will be imported, including case.

from util import attr

class ConformanceLevels(object):
    Basic = 0
    Optional = 1
    Intermediate = 2
    Advanced = 3
cl = ConformanceLevels()
    
class TypeMap(object):
    "Map types to those needed by the database."
    char = 'char'
    string = 'varchar'
    integer = 'integer'
    clob = 'clob'
    blob = 'blob'
    date = 'date'
    time = 'time'
    timestamp = 'timestamp'
    serial = 'serial'
    
class DriverBase(object):
    """Describes the features that are known to vary between drivers.
    Drivers should subclass & set attributes as appropriate.
    """
    def convert_connect_args(self, ConnectionInfo):
        """Subclasses should implement & return a args, kwargs tuple 
        that will be passwed to the driver's connect method
        """
        raise NotImplementedError

    def get_create_db_cmd(self, db_name):
        """ The command used to create a database. Return None when dbs are
        created implicitly.
        """
        raise NotImplementedError

    transactional_ddl = attr(True, 
            doc = "DDL statements are transactional (need commit)")

    connection_level_exceptions = attr(True,
            doc = "Exceptions are defined at the connection level.",
            conformance_level = cl.Optional)

    rollback_defined = attr(True, 
            doc = "Driver defines rollback",
            conformance_level = cl.Intermediate)

    call_proc = attr(True, 
            doc = "Database supports stored procedures",
            conformance_level = cl.Advanced)

    explicit_db_create = attr(True, 
            doc = "Databases are created explicitly (here for SQLite)")

    authentication = attr(True, 
            doc = "Database requires authentication (for SQLite)")
    
    inoperable_closed_connections = attr(True,
            doc = "Closed connections are no longer usable",
            conformance_level = cl.Basic)
    
    sane_empty_fetch = attr(True,
            doc = "Fetch should fail if no query is issued",
            conformance_level = cl.Basic)

    sane_rowcount = attr(True,
            doc = "Rowcount should be set correctly by fetchmany",
            conformance_level = cl.Intermediate)

    rowcount_reset_empty_fetch = attr(True,
            doc = "Rowcount is reset after an empty fetch",
            conformance_level = cl.Basic)

    driver_level_datatypes = attr(True,
            doc = "Available datatypes are defined at the driver level",
            conformance_level = cl.Optional)

    driver_level_datatypes_binary = attr(True,
            doc = "The Binary datatype is defined at the driver level",
            conformance_level = cl.Optional)

    time_datatype = attr(True,
            doc = "Driver supports the time datatype (optional)",
            conformance_level = cl.Optional)

    time_datatype_time = attr(True,
            doc = "The driver's time datatype supports python time values",
            conformance_level = cl.Intermediate)

    time_datatype_subsecond = attr(True,
            doc = "The time datatype supports subsecond times")

    timestamp_datatype_subsecond = attr(True,
            doc = "The timestamp datatype supports subsecond times")

    sane_timestamp = attr(True,
            doc = "Timestamp returns datetime compatible timestamps",
            conformance_level = cl.Intermediate)

    setoutputsize = attr(True,
            doc = "Driver supports setoutputsize",
            conformance_level = cl.Optional)
    
    stored_procedure_language = attr("SQL:2003",
            doc = "Stored procedure language can be one of: " 
                  "Transact-SQL (Microsoft SQL Server), PL/SQL (Oracle), SQL/PL (DB2), "
                  "PL/pgSQL (PostgreSQL), SQL:2003 (Anything standards compliant (MySQL))")

    callproc = attr(True,
            doc = "Database support stored procedures (Optional)",
            conformance_level = cl.Optional)

    lower_func = attr('lower',
            doc = "The name of the function used to convert a string to lowercase")

    dbapi_level = attr("2.0",
            doc = "The DB-API level that the driver supports")

    scrollable_cursors = attr(False,
            doc = "Driver supports scrollable cursors",
            conformance_level = cl.Advanced)

    blob_binary = attr(True,
            doc = "BLOBs can be created from the driver's Binary type", 
            conformance_level = cl.Basic)

    smart_lob_open = attr(False,
            doc = "LOBs can be read from a file handle",
            conformance_level = cl.Advanced)

    lastrowid = attr(True,
            doc = "Supports lastrowid",
            conformance_level = cl.Basic)


class pysqlite2(DriverBase):

    def convert_connect_args(self, ConnectionInfo):
        return [ConnectionInfo.database], dict()

    def get_create_db_cmd(self, db_name):
        return None

    explicit_db_create = False
    inoperable_closed_connections = False
    authentication = False
    sane_empty_fetch = False
    driver_level_datatypes = False
    time_datatype = True
    transactional_ddl = False
    sane_rowcount = False
    sane_empty_fetch = False
    time_datatype_time = False

    typemap = TypeMap()

class psycopg2(DriverBase):
    def convert_connect_args(self, ci):
        kwargs = {'dsn':'host=%s dbname=%s user=%s password=%s' %
                   (ci.hostname, ci.database, ci.username, ci.password)}
        return [], kwargs

    def get_create_db_cmd(self, db_name):
        return "psql -c 'create database %s'" % db_name

    rowcount_reset_empty_fetch = False
    stored_procedure_language = "PL/pgSQL"

    typemap = TypeMap()
    typemap.clob = 'text'
    typemap.blob = 'bytea'

class MySQLdb(DriverBase):
    def convert_connect_args(self, ci):
        kwargs = dict(
            host = ci.hostname,
            user = ci.username,
            passwd = ci.password,
            db = ci.database
        )
        return [], kwargs

    def get_create_db_cmd(self, db_name):
        raise NotImplementedError

    time_datatype_subsecond = True
    timestamp_datatype_subsecond = False
    sane_timestamp = False
    sane_empty_fetch = False
    setoutputsize = False
    rowcount_reset_empty_fetch = False
  
    typemap = TypeMap()
    typemap.clob = 'text'

class ibm_db(DriverBase):
    def convert_connect_args(self, ci):
        if ci.port:
            args =[
               "DATABASE=%s;HOSTNAME=%s;PORT=%s;PROTOCOL=TCPIP;UID=%s;PWD=%s;"
               % (ci.database, ci.hostname, ci.port, ci.username, ci.password)
            ]
        else:
            args = ["DATABASE=%s;UID=%s;PWD=%s;"
                    % (ci.database, ci.name, ci.password)]

    def get_create_db_cmd(self, db_name):
        return "db2 create database %s" % db_name

    typemap = TypeMap()
    typemap.serial = "int generated by default as identity"

class ceODBC(DriverBase):
    time_datatype = False
    time_datatype_time = False
    time_datatype_subsecond = False
    connection_level_exceptions = False
    typemap = TypeMap()
    typemap.date = "datetime"
    typemap.time = "integer"
    typemap.serial = "integer"
    typemap.clob = "text"
    typemap.blob = "image"

    def convert_connect_args(self, ci):
        return [ci.database], {}

class cx_Oracle(DriverBase):
    time_datatype = False
    time_datatype_time = False
    time_datatype_subsecond = False
    connection_level_exceptions = False
    typemap = TypeMap()
    typemap.string = "varchar2"
    typemap.time = "number"
    typemap.serial = "number"

    def convert_connect_args(self, ci):
        return [ci.username, ci.password, ci.database], {}

