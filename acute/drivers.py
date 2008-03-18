#!/usr/bin/env python

# See the README for details on how this module works (if it's not obvious).

# NOTES: 
# When subclassing DriverBase, be sure to match the name of the driver 
#    that will be imported, including case.
import databases
from util import attr

class ConformanceLevels(object):
    Basic = 0
    Optional = 1
    Intermediate = 2
    Advanced = 3
cl = ConformanceLevels()
    
    
class DriverBase(object):
    """Describes the features that are known to vary between drivers.
    Drivers should subclass & set attributes as appropriate.
    """
    def convert_connect_args(self, ConnectionInfo):
        """Subclasses should implement & return a args, kwargs tuple 
        that will be passwed to the driver's connect method
        """
        raise NotImplementedError

    dbms = attr("TDB",
        doc = "The databases.DatabaseBase class that defines the"
            " dbms' capabilities."
        )

    connection_level_exceptions = attr(True,
            doc = "Exceptions are defined at the connection level.",
            conformance_level = cl.Optional)

    rollback_defined = attr(True, 
            doc = "Driver defines rollback",
            conformance_level = cl.Intermediate)

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

    time_datatype_time = attr(True,
            doc = "The driver's time datatype supports python time values",
            conformance_level = cl.Intermediate)

    sane_timestamp = attr(True,
            doc = "Timestamp returns datetime compatible timestamps",
            conformance_level = cl.Intermediate)

    setoutputsize = attr(True,
            doc = "Driver supports setoutputsize",
            conformance_level = cl.Optional)
    
    dbapi_level = attr("2.0",
            doc = "The DB-API level that the driver supports")

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

    dbms = databases.sqlite

    inoperable_closed_connections = False
    sane_empty_fetch = False
    driver_level_datatypes = False
    sane_rowcount = False
    sane_empty_fetch = False
    time_datatype_time = False


class psycopg2(DriverBase):
    def convert_connect_args(self, ci):
        kwargs = {'dsn':'host=%s dbname=%s user=%s password=%s' %
                   (ci.hostname, ci.database, ci.username, ci.password)}
        return [], kwargs

    dbms = databases.postgres

    rowcount_reset_empty_fetch = False


class MySQLdb(DriverBase):
    def convert_connect_args(self, ci):
        kwargs = dict(
            host = ci.hostname,
            user = ci.username,
            passwd = ci.password,
            db = ci.database
        )
        return [], kwargs

    dbms = databases.mysql 

    sane_timestamp = False
    sane_empty_fetch = False
    setoutputsize = False
    rowcount_reset_empty_fetch = False
  

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

    dbms = databases.db2

class ceODBC(DriverBase):
    connection_level_exceptions = False

    def convert_connect_args(self, ci):
        return [ci.database], {}

class cx_Oracle(DriverBase):
    connection_level_exceptions = False

    def convert_connect_args(self, ci):
        return [ci.username, ci.password, ci.database], {}

    dbms = databases.oracle

