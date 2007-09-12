#!/usr/bin/env python

# See the README for details on how this module works (if it's not obvious).

# NOTES: 
# 1) When subclassing DriverBase, be sure to match the name of the driver 
#    that will be imported, including case.
# 2) The docstrings for each class attribute are stored in a seperate 
#    attribute that follows the naming convention "_ATTRIBUTE__doc__".  
#    This allows the introspection mechanism of report.py to work.

#class TypeMapping(object):
    
class DriverBase(object):
    """Describes the features that are known to vary between drivers.
    Class attributes are used to set the default for every feature. These are
    overridden for the drivers as necessary when the class is instatiated.
    """

    def get_create_db_cmd(db_name):
        """ The command used to create a database. Return None when dbs are
        created implicitly.
        """
        raise NotImplementedError

    transactional_ddl = True
    _transactional_ddl__doc__ = "DDL statements are transactional (need commit)"

    connection_level_exceptions = True
    _connection_level_exceptions__doc__ = (
        "Exceptions are defined at the connection level (optional)")

    rollback_defined = True
    _rollback_defined__doc__ = "Driver defines rollback"

    call_proc = True
    _call_proc__doc__ = "Database supports stored procedures"

    explicit_db_create = True
    _explicit_db_create__doc__ = (
        "Databases are created explicitly (here for SQLite)")

    authentication = True
    _authentication__doc__ = "Database requires authentication (for SQLite)"
    
    inoperable_closed_connections = True
    _inoperable_closed_connections__doc__ = (
        "Closed connections are no longer usable")
    
    sane_empty_fetch = True
    _sane_empty_fetch__doc__ = "Fetch should fail if no query is issued"

    sane_rowcount = True
    _sane_rowcount__doc__ = "Rowcount should be set correctly by fetchmany"

    rowcount_reset_empty_fetch = True
    _rowcount_reset_empty_fetch__doc__ = (
        "Rowcount is reset after an empty fetch")

    driver_level_datatypes = True
    _driver_level_datatypes__doc__ = (
        "Available datatypes are defined at the driver level")

    driver_level_datatypes_binary = True
    _driver_level_datatypes_binary__doc__ = (
        "The Binary datatype is defined at the driver level")

    time_datatype = True
    _time_datatype__doc__ = "Driver supports the time datatype (optional)"

    time_datatype_time = True
    _time_datatype_time__doc__ = (
        "The driver's time datatype supports python time values")

    time_datatype_subsecond = True
    _time_datatype_subsecond__doc__ = (
        "The time datatype supports subsecond times")

    timestamp_datatype_subsecond = True
    _timestamp_datatype_subsecond__doc__ = (
        "The timestamp datatype supports subsecond times")

    sane_timestamp = True
    _sane_timestamp__doc__ = "Timestamp returns sane timestamps"

    setoutputsize = True
    _setoutputsize__doc__ = "Driver supports setoutputsize"
    
    serial_key_def = 'int'
    _serial_key_def__doc__ = "Column definition to use for serial keys"
    
    blob_type = 'blob'
    _blob_type__doc__ = "Column definition to use for BLOBs"
    
    clob_type = 'clob'
    _clob_type__doc__ = "Column definition to use for CLOBs"
    
    stored_procedure_language = "SQL:2003"
    _stored_procedure_language__doc__ =  (
        "Stored procedure language can be one of: " 
        "Transact-SQL (Microsoft SQL Server), PL/SQL (Oracle), SQL/PL (DB2), "
        "PL/pgSQL (PostgreSQL), SQL:2003 (Anything standards compliant (MySQL))")

    callproc = True
    _callproc__doc__ = "Database support stored procedures (Optional)"

    lower_func = 'lower'
    _lower_func__doc__ = (
        "The name of the function used to convert a string to lowercase")

    dbapi_level = "2.0"
    _dbapi_level__doc__ = "The DB-API level that the driver supports"

    scrollable_cursors = False
    _scrollable_cursors__doc__ = "Driver supports scrollable cursors"

    blob_binary = True
    _blob_binary__doc__ = "BLOBs can be created from the driver's Binary type"

    smart_lob_open = False
    _smart_lob_open__doc__ = "LOBs can be read from a file handle"

    lastrowid = True
    _lastrowid__doc__ = "Supports lastrowid"


class pysqlite2(DriverBase):
    def get_create_db_cmd(db_name):
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

class psycopg2(DriverBase):
    def get_create_db_cmd(db_name):
        return "psql -c 'create database %s'" % db_name

    serial_key_def = 'serial'
    rowcount_reset_empty_fetch = False
    clob_type = 'text'
    blob_type = 'bytea'
    stored_procedure_language = "PL/pgSQL"

class MySQLdb(DriverBase):
    def get_create_db_cmd(db_name):
        raise NotImplementedError

    clob_type = "text"
    time_datatype_subsecond = True
    timestamp_datatype_subsecond = False
    sane_timestamp = False
    sane_empty_fetch = False
    setoutputsize = False
    rowcount_reset_empty_fetch = False

class ibm_db(DriverBase):
    def get_create_db_cmd(db_name):
        return "db2 create database %s" % db_name

    serial_key_def = "int generated by default as identity"

