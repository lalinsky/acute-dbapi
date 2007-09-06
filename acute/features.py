#!/usr/bin/env python
class SupportedFeatures(object):
    """ Describes the features that are known to vary between DB-API implementations.
    Class attributes are used to set the default for all available features. These are
    overridden as necessary when the class is instatiated with a known driver name.
    """
    
    def __init__(self, driver_name): 
        """ Return the features supported by a given driver.
        The driver should be passed by name
        """
        self._driver_name = driver_name
        if driver_name == 'pysqlite2': 
            self.explicit_db_create = False
            self.inoperable_closed_connections = False
            self.authentication = False
            self.sane_empty_fetch = False
            self.driver_level_datatypes = False
            self.time_datatype = True
            self.transactional_ddl = False
            self.callproc = False
            self.sane_rowcount = False
            self.time_datatype_time = False
            self.blob_binary = False
        elif driver_name == 'psycopg2':
            self.serial_key_def = 'serial'
            self.callproc = True
            self.rowcount_reset_empty_fetch = False
            self.clob_type = 'text'
            self.blob_type = 'bytea'
            self.stored_procedure_language = "PL/pgSQL"
        elif driver_name == 'MySQLdb':
            self.clob_type = "text"
            self.time_datatype_subsecond = False
        elif driver_name == 'pydb2':
            self.serial_key_def = "int generated by default as identity"

    """ Are DDL statements are transactional in nature? (ie, need commit())"""
    transactional_ddl = True
    """ Are exceptions defined at the connection level? (Optional in DB-API 2.0)"""
    connection_level_exceptions = True
    """ Is rollback defined? """
    rollback_defined = True
    """ Are stored procedures availabled? """
    call_proc = True
    """ Are databases created explicitly?  Mostly here for SQLite """
    explicit_db_create = True
    """ Does database require authentication?  Most here for SQLite """
    authentication = True
    
    """ A closed connection should not be usable anymore. """
    inoperable_closed_connections = True
    """ Fetch should fail if no query is issued. """
    sane_empty_fetch = True
    """ Rowcount should be set currectly by fetchmany. """
    sane_rowcount = True
    """ Rowcount should be reset after an empty fetch. """
    rowcount_reset_empty_fetch = True
    """ Available datatypes should be defined at the driver level. """
    driver_level_datatypes = True
    """ Specifically, is the Binary datatype defined at driver level? """
    driver_level_datatypes_binary = True
    """ Does the driver support the time datatype? (Optional) """
    time_datatype = True
    """ Does the time datatype support python time values? """
    time_datatype_time = True
    """ Does the time datatype support subsecond times? """
    time_datatype_subsecond = True
    
    
    """ How are serial keys defined in the database? """
    serial_key_def = 'int'
    """ How are BLOBs defined in the database? """
    blob_type = 'blob'
    """ How are CLObs defined in the database? """
    clob_type = 'clob'
    
    """ Stored procedure language can be one of:
    Transact-SQL (for Microsoft SQL Server)
    PL/SQL (for Oracle)
    SQL/PL (for DB2),
    PL/pgSQL (for PostgreSQL)
    SQL:2003 (for anything that adheres to the standard, like MySQL)
    """
    stored_procedure_language = "SQL:2003"
    
    
    """ Does the DB support stored procedures? (Optional)"""
    callproc = True    
    """ The name of the function used to convert a string to lowercase """
    lower_func = 'lower'
    """ The DB-API level that the driver is known to support """
    dbapi_level = "2.0"
    """ Whether the driver supports scrollable cursors """
    scrollable_cursors = False
    """ Can BLOBs be created from the driver's Binary type? """
    blob_binary = True
    """ Whether LOBs can be read from a file handle """
    smart_lob_open = False
    """ Whether lastrowid is supported """
    lastrowid = True
    
    
