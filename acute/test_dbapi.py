#!/usr/bin/env python
''' Python DB API 2.0 driver compliance unit test suite.
Only a few 'optional extensions' are being tested at this point.
'''
#TODO: Use assertRaises from ActiveState scripts
#TODO: Fix this all the tests that require 'amiracle' (These tests are skipped).
#TODO: Create a test that uses primary keys.  Test errhandling with it.

__rcs_id__  = '$Id$'
__version__ = '$Revision$'[11:-2]
__author__ = 'Ken Kuhlman <acute@redlagoon.net>'
# $Log: dbapi20.py,v $

import unittest
import time
import datetime
import popen2
import config
import util
from util import OrderedDict, connect, connect_plus_cursor, TableBase
import decorators
from decorators import requires, raises
import drivers
import warnings

table_prefix = config.table_prefix
driver_name = config.driver_name
driver_meta= getattr(drivers, driver_name)()
dbms_meta = driver_meta.dbms()

decorators.register_supported_features(driver_meta, dbms_meta)

driver_module = util.import_module(driver_name)

tm = dbms_meta.typemap
#TODO: Change to be table per column?  Or just make _insert smarter?
class Booze(TableBase):
    name = '%sbooze' % table_prefix
    ddl = ('create table %s (name %s(20))' % (name, tm.string))

class Barflys(TableBase):
    name = '%sbarflys' % table_prefix
    ddl = ('create table %s (id %s, name %s(20))' % 
        (name, tm.serial, tm.string))

class TestTypes(TableBase): 
    name = '%stesttypes' % table_prefix
    ddl = ("""create table %stesttypes (
        int_fld %s,
        varchar1 %s(3),
        date1 %s,
        timestamp1 %s,
        time1 %s,
        clob1 %s,
        blob1 %s
        )"""
        % (table_prefix, tm.serial, tm.string, tm.date, tm.timestamp,
           tm.time, tm.clob, tm.blob)
        )

tables = [Booze, Barflys, TestTypes]

def setup_module():
    "Create the tables used in the tests. Also create the db if needed."
    try:
        con = connect()
    except:
        try:
            create_db_cmd = dbms_meta.get_create_db_cmd(
                config.ConnectionInfo.database)
        except NotImplementedError:
            create_db_cmd = ''

        if create_db_cmd:
            cout, cin = popen2.popen2(create_db_cmd)
            cin.close()
            cout.read()
            con = connect()
        else:
            raise Exception("Can't connect to database and no "
                  "create command given")

    cs = con.cursor() 
    for table in tables:
        table.create(con = con, cur = cs)
    con.close()
    return

def teardown_module():
    con = connect()
    for table in tables:
        try:
            table.drop()
        except driver_module.Error:
            warnings.warn("Drop on table %s failed" % table.name)
    con.close()


class AcuteBase(unittest.TestCase):
    """ Base class for the tests. 
    Defines basic setup, Teardown, _connect methods.
    """

    # The name of the driver & the driver itself (as imported)
    driver_name = driver_name
    driver = driver_module

    # Keyword arguments for connect
    connection_info = config.ConnectionInfo()

    def tearDown(self):
        try:
            self.con.rollback()
        except:
            pass

    def _connect(self, *args, **kwarg):
      con = connect(*args, **kwarg)
      self.con = con
      return con

    def _insert(self, con, cur, table=None, data=None, stmt_type='insert'):
        if not table:
            table = Booze
        if not data:
            data = dict(name="Coopers")
        cols = ", ".join(data)

        stmt_base = 'insert into %s (%s) values' % (table.name, cols)
        if stmt_type == 'select':
            stmt_base = 'select * from %s where %s = ' % (
                table.name, data.keys()[0])

        data_keys = data.keys()
        markers = []
        for xx in range(len(data_keys)):
            if self.driver.paramstyle == 'qmark':
                marker = '?'
            elif self.driver.paramstyle == 'numeric':
                marker = '(:%s)' % (xx + 1)
            elif self.driver.paramstyle == 'format':
                marker = '(%s)'
            elif self.driver.paramstyle == 'named':
                marker = '(:%s)' % data_keys[xx]
            elif self.driver.paramstyle == 'pyformat':
                marker = '(%(' + data_keys[xx] + ')s)'

            markers.append(marker)
        stmt = "%s(%s)" % (stmt_base, ", ".join(markers))

        if self.driver.paramstyle in ('qmark', 'numeric', 'format'):
            cur.execute(stmt, data.values())
        elif self.driver.paramstyle in ('named', 'pyformat'):
            cur.execute(stmt, data)
        else:
            self.fail('Invalid paramstyle')        
        con.commit()

class TestModule(AcuteBase):
    """ Modules define certain attributes"""

    def test_connect(self):
        "Can connect to database"
        con = self._connect()
        con.close()

    def test_apilevel(self):
        "Driver defines apilevel"
        self.failUnless(hasattr(self.driver, "apilevel"), 
            "Driver must define apilevel")
        self.assertEqual(self.driver.apilevel, driver_meta.dbapi_level,
            "Driver supports different version of DBAPI than the testsuite")

    def test_threadsafety(self):
        "Driver defines threadsafety"
        self.failUnless(hasattr(self.driver, "threadsafety"), 
            "Driver must define threadsafety")
        self.failUnless(self.driver.threadsafety in (0,1,2,3), 
            "Threadsafety not in allowed values")

    def test_globalparamstyle(self):
        "Driver defines paramstyle"
        self.failUnless(hasattr(self.driver, "paramstyle"), 
            "Driver must define paramstyle")
        paramstyles = ('qmark','numeric','named','format','pyformat')
        self.failUnless(self.driver.paramstyle in paramstyles, 
             "Paramstyle not in allowed values")  

    def test_Exceptions(self):
        """Required exceptions are in the defined heirachy."""
        self.failUnless(issubclass(self.driver.Warning,StandardError))
        self.failUnless(issubclass(self.driver.Error,StandardError))
        self.failUnless(
            issubclass(self.driver.InterfaceError,self.driver.Error)
            )
        self.failUnless(
            issubclass(self.driver.DatabaseError,self.driver.Error)
            )
        self.failUnless(
            issubclass(self.driver.OperationalError,self.driver.Error)
            )
        self.failUnless(
            issubclass(self.driver.IntegrityError,self.driver.Error)
            )
        self.failUnless(
            issubclass(self.driver.InternalError,self.driver.Error)
            )
        self.failUnless(
            issubclass(self.driver.ProgrammingError,self.driver.Error)
            )
        self.failUnless(
            issubclass(self.driver.NotSupportedError,self.driver.Error)
            )

#TODO: pyscopg2 fails these because it's returning a string. Move to 'intermediate'?
#TODO:  -- Date(2007, 05, 01).adapted works though
class TestModuleDatatypes(AcuteBase):
    """ Test module level datatypes.  
    The TestTypesEmbedded class below tests their use in SQL statements.
    """
    driver = driver_module
    
    def test_DateFromTicks(self):
        'Module supports DateFromTicks'
        d = self.driver.DateFromTicks(6798)

    @requires('time_datatype')
    def test_TimeFromTicks(self):
        'Module supports TimeFromTicks'
        t = self.driver.TimeFromTicks(6798)

    def test_TimestampFromTicks(self):
        'Module supports TimestampFromTicks'
        ts = self.driver.TimestampFromTicks(6798)
        
    #TODO: More datatype tests exist in TestTypes. Consolidate or split these?
    def test_Date(self):
        'Module supports Date and DateFromTicks'
        d1 = self.driver.Date(2002,12,25)
        d2 = self.driver.DateFromTicks(time.mktime((2002,12,25,0,0,0,0,0,0)))
        # Can we assume this? API doesn't specify, but it seems implied
        self.assertEqual(str(d1),str(d2))

    @requires('time_datatype')
    def test_Time(self):
        'Module supports Time and TimeFromTicks'
        t1 = self.driver.Time(13,45,30)
        t2 = self.driver.TimeFromTicks(time.mktime((2001,1,1,13,45,30,0,0,0)))
        # Can we assume this? API doesn't specify, but it seems implied
        self.assertEqual(str(t1),str(t2))

    @requires('sane_timestamp')
    def test_Timestamp(self):
        'Module supports Timestamp and TimestampFromTicks'
        t1 = self.driver.Timestamp(2002,12,25,13,45,30)
        t2 = self.driver.TimestampFromTicks(
            time.mktime((2002,12,25,13,45,30,0,0,0))
            )
        # Can we assume this? API doesn't specify, but it seems implied
        self.assertEqual(str(t1), str(t2))

    @requires('driver_level_datatypes_binary')
    def test_Binary(self):
        'Module supports Binary'
        b = self.driver.Binary('Something')
        b = self.driver.Binary('')

    @requires('driver_level_datatypes')
    def test_STRING(self):
        'Module defines STRING'
        self.driver.STRING

    @requires('driver_level_datatypes')
    def test_BINARY(self):
        'Module defines BINARY'
        self.driver.BINARY
  
    @requires('driver_level_datatypes')
    def test_NUMBER(self):
        'Module defines NUMBER'
        self.driver.NUMBER

    @requires('driver_level_datatypes')
    def test_DATETIME(self):
        'Module defines DATETIME'
        self.driver.DATETIME
  
    @requires('driver_level_datatypes')
    def test_ROWID(self):
        'Module defines ROWID'
        self.driver.ROWID
        
    def test_date(self):
        "Module's date is equivalent to datetime's date"
        #TODO: Postgres probably shouldn't pass this test..
        #print self.driver.Date(2007, 05, 01)
        #print datetime.date(2007, 05, 01)
        if self.driver_name == 'psycopg2':
            self.assertEqual(self.driver.Date(2007, 05, 01).adapted,  
                         datetime.date(2007, 05, 01))
        else:
            self.assertEqual(self.driver.Date(2007, 05, 01),
                         datetime.date(2007, 05, 01))

    @requires('time_datatype')
    def test_time(self):
        "Module's time attribute is equivalent to datetime's time"
        #TODO: Perhaps dropping str() makes it an intermediate test?
        #self.assertEqual(self.driver.Time(11, 03, 13), 
        #                 datetime.time(11, 03, 13))
        if self.driver_name == 'psycopg2':
            self.assertEqual(self.driver.Time(11, 03, 13).adapted, 
                         datetime.time(11, 03, 13))
        else:
            self.assertEqual(str(self.driver.Time(11, 03, 13)), 
                         str(datetime.time(11, 03, 13)))

    def test_timestamp(self):
        "Module's Timestamp attribute is equivalent to datetime's datetime"
        if self.driver_name == 'psycopg2':
            self.assertEqual(
                str(self.driver.Timestamp(2007, 05, 01, 11, 03, 13).adapted),
                str(datetime.datetime(2007, 05, 01, 11, 03, 13)))
        else:
            self.assertEqual(
                self.driver.Timestamp(2007, 05, 01, 11, 03, 13),
                datetime.datetime(2007, 05, 01, 11, 03, 13))

    @requires('binary_buffer')
    def test_binary(self):
        """Binary type should be compatible with buffers."""
        #TODO: Inserted str()s here for psycopg2.  Add another test without?
        self.assertEqual(str(self.driver.Binary(chr(0) + "'")),
                         str(buffer(chr(0) + "'")))

class TestConnection(AcuteBase):
    #TODO: Add a set of tests that are more specific about which errors are thrown.
    expected_error = driver_module.Error 

    def test_success(self):
        """Successful connect and close"""
        self._connect()
        self.con.close()

    def test_close_commit(self):
        """Can't commit a closed connection"""
        con = connect()
        con.close()
        self.assertRaises(self.expected_error, con.commit)

    @requires('inoperable_closed_connections_close')
    def test_close_close(self):
        """Can't close a closed connection """
        con = connect()
        con.close()
        self.assertRaises(self.expected_error, con.close)

    @requires('inoperable_closed_connections')
    def test_close_rollback(self):
        """Can't rollback a closed connection"""
        con = connect()
        con.close()
        self.assertRaises(self.expected_error, con.rollback)

    @requires('inoperable_closed_connections')
    @requires('inoperable_closed_connections_cursor')
    def test_close_cursor(self):
        """Can't get a new cursor on a closed connection"""
        con = connect()
        con.close()
        self.assertRaises(self.expected_error, con.cursor)

    @requires('inoperable_closed_connections')
    def test_close_execute(self):
        """Can't execute on a cursor with a closed connection"""
        # pysqlite2 raises ProgrammingError, while pyscopg2, MySQLdb,
        #  and ibmdb raise InterfaceError.  There's no standard here
        #  so let drivers get away with any subclass of Error.
        con, cs = connect_plus_cursor()
        con.close()

        qry = "select * from %s" % Booze.name
        self.assertRaises(self.expected_error, cs.execute, qry)

    @requires('explicit_db_create')
    def test_bogusDB(self):
        """Connection should fail using bogus database"""
        connection_info = config.ConnectionInfo()
        connection_info.database = 'NonexistentDatabase'
        self.assertRaises(self.expected_error, 
                          self._connect, connection_info)

    @requires('authentication')
    def test_bogusUser(self):
        """Connection should fail using bogus username"""
        connection_info = config.ConnectionInfo()
        connection_info.username = 'kingarthur'
        self.assertRaises(self.expected_error,  
                          self._connect, connection_info)

    @requires('authentication')
    def test_bogusPwd(self):
        """Connection should fail using bogus password"""
        connection_info = config.ConnectionInfo()
        connection_info.password = 'xyzzy'
        self.assertRaises(self.expected_error,
                          self._connect, connection_info)

    @requires('authentication')
    def test_missingPwd(self):
        """Connection should fail using blank password"""
        connection_info = config.ConnectionInfo()
        connection_info.password = ''
        self.assertRaises(self.expected_error, 
                          self._connect, connection_info)
     
    def test_commit_nochange(self):
        """Consecutive commits should be successfull"""
        self._connect()
        self.con.commit()
        self.con.commit()

    def test_rollback_nochange(self):
        """Consecutive rollbacks should be successfull"""
        self._connect()
        self.con.rollback()
        self.con.rollback()

    def test_cursor_create(self):
        """Connections need to be able to create cursors"""
        self._connect()
        self.failUnless(self.con.cursor(), "unable to create a cursor")

    @requires('connection_level_exceptions')
    def test_ExceptionsAsConnectionAttributes(self):
        """ Connection objects should include the exceptions
        as attributes (optional)
        """
        con = self._connect()
        drv = self.driver
        self.failUnless(con.Warning is drv.Warning)
        self.failUnless(con.Error is drv.Error)
        self.failUnless(con.InterfaceError is drv.InterfaceError)
        self.failUnless(con.DatabaseError is drv.DatabaseError)
        self.failUnless(con.OperationalError is drv.OperationalError)
        self.failUnless(con.IntegrityError is drv.IntegrityError)
        self.failUnless(con.InternalError is drv.InternalError)
        self.failUnless(con.ProgrammingError is drv.ProgrammingError)
        self.failUnless(con.NotSupportedError is drv.NotSupportedError)

    def test_commit(self):
        """ Commit must be defined, even if it doesn't do anything """
        con = self._connect()
        try:
            con.commit()
        finally:
            con.close()

    @requires('rollback_defined')
    def test_rollback(self):
        """ Rollback must work or throw NotSupportedError."""
        #The spec allows drivers that don't support rollback to also 
        #simply not define this method, which is silly.  2 ways to do the same
        #trivial thing!
        #TODO: Suggest patch to PEP 249
        con = self._connect()
        if hasattr(con,'rollback'):
            try:
                con.rollback()
            except self.driver.NotSupportedError:
                pass

class TestCursor(AcuteBase):
    #TODO: Test lastrowid after bogus operations like ddl, or insert on table w/out rowid
    #TODO: Test not null violations, esp. against PKs. (pysqlite was failing)
    def test_cursor(self):
        """ Connections must have cursor method """
        con = self._connect()
        try:
            cur = con.cursor()
        finally:
            con.close()
    
    @requires('lastrowid', 'auto_serial')
    def test_lastrowid(self):
        "Insert into identity column sets cursor.lastrowid"
        con, cs = Barflys.create()
        
        data = dict(id=None, name='Joe')
        self._insert(con, cs, table=Barflys, data=data )
        self.failUnlessEqual(cs.lastrowid, 1)
        self.failUnlessEqual(cs.rowcount, 1)
        
    def test_insert_None(self):
        "Insert a row with Null columns"
        con, cs = Booze.create()
        self._insert(con, cs, data=dict(name=None))
        cs.execute("select name from %sbooze" % table_prefix)
        rows = cs.fetchall()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][0], None)
        #id_value = self.cs.lastrowid()
        #self.assertEqual(1, id_value)

    @requires('amiracle')
    def test_insert_type_mismatch(self):
         "Insert using the wrong datatype raises TypeError"
         Booze.create()
         self.assertRaises(TypeError, self._insert, (1.0, None))

    @requires('amiracle')
    def test_insert_truncation(self):
         "Insert that overflows column size raises ProgrammingError"
         Booze.create()
         self.assertRaises(driver_module.ProgrammingError,
             self._insert, (1, 'XXXX'))

    @requires('amiracle')
    def test_insert_parm_mismatch(self):
        "Inserting wrong number of columns raises ProgrammingError"
        Booze.create()
        self.assertRaises(driver_module.ProgrammingError, self._insert, (1, ))

    def test_arraysize(self):
        "Cursor must define arraysize"
        con, cur = connect_plus_cursor()
        cur.arraysize

    def test_setinputsizes_basic(self):
        "Insert works with cursor.setinputsize"
        con, cur = connect_plus_cursor()
        try:
            cur.setinputsizes( (25,) )
            self._insert(con, cur)
        finally:
            con.close()

    @requires('setoutputsize')
    def test_setoutputsize_basic(self):
        "Insert works with cursor.setoutputsize"
        con, cur = connect_plus_cursor()
        try:
            cur.setoutputsize(1000)
            cur.setoutputsize(2000,0)
            self._insert(con, cur)
        finally:
            con.close()

    #TODO: Determine approaches used by the different drivers
    #def test_setoutputsize(self):
    #    # Real test for setoutputsize is driver dependant
    #    raise NotImplementedError,'Driver need to override this test'
   
    @requires('transaction_isolation')
    def test_cursor_isolation(self):
        "A cursor can read it's own uncommited data"
        #TODO: Split the 2 connection test into it's own unit.
        con = self._connect()
        con2 = self._connect()
        try:
            cur1 = con.cursor()
            cur2 = con.cursor()
            cur3 = con2.cursor()
            cur1.execute("insert into %s values ('Victoria Bitter')" % (
                Booze.name
                ))
            cur2.execute("select name from %s" % Booze.name)
            cur3.execute("select name from %s" % Booze.name)
            booze = cur2.fetchall()
            self.assertEqual(len(booze),1)
            self.assertEqual(len(booze[0]),1)
            self.assertEqual(booze[0][0],'Victoria Bitter')
            #con.rollback()
            booze2 = cur3.fetchall()
            self.assertEqual(len(booze2), 0)
        finally:
            con.close()
            con2.close()

    def test_description(self):
        "Cursor description describes columns correctly"
        con, cur = Booze.create()
        try:
            self.assertEqual(cur.description,None,
                "cursor.description should be none after executing a "
                "statement that can't return rows (such as DDL)"
                )
            cur.execute('select name from %s' % Booze.name)
            self.assertEqual(len(cur.description),1,
                'cursor.description describes too many columns'
                )
            self.assertEqual(len(cur.description[0]),7,
                'cursor.description[x] tuples must have 7 elements'
                )
            self.assertEqual(cur.description[0][0].lower(),'name',
                'cursor.description[x][0] must return column name'
                )
            #TODO: Break this out into own test?
            if driver_name != 'pysqlite2':
                self.assertEqual(cur.description[0][1],self.driver.STRING,
                  'cursor.description[x][1] must return column type. Got %r'
                    % cur.description[0][1]
                  )

            Barflys.create(con = con, cur = cur)
            self.assertEqual(cur.description,None,
                'cursor.description not being set to None when executing '
                'no-result statements (eg. DDL)'
                )
        finally:
            con.close()

    #TODO: Test rowcount with scrollable cursors?
    @requires('rowcount_reset_empty_fetch')
    def test_rowcount(self):
        "Rowcount matches the number of rows inserted"
        #TODO: What about updates/deletes?
        con, cur = connect_plus_cursor()
        Booze.create()
        try:
            #TODO: Check this against PEP 249.  Original code claimed -1 was correct answer
            if driver_meta.sane_rowcount:
                self.assertEqual(cur.rowcount, 0,
                    'cursor.rowcount should be 0 after executing no-result '
                    'statements, not %s' % cur.rowcount
                    )
            cur.execute("insert into %s values ('Victoria Bitter')" % (
                Booze.name
                ))
            self.failUnless(cur.rowcount in (-1,1),
                'cursor.rowcount should == number or rows inserted, or '
                'set to -1 after executing an insert statement'
                )
            cur.execute("select name from %s" % Booze.name)
            #TODO: Move to own test.
            if driver_meta.sane_empty_fetch:
                self.failUnless(cur.rowcount in (-1,1),
                    'cursor.rowcount should == number of rows returned, or '
                    'set to -1 after executing a select statement, not %s.'
                    % cur.rowcount
                    )
            Barflys.create(con = con, cur = cur)
            #TODO: Check this against PEP 249.  Original code claimed -1 was correct answer
            if driver_meta.sane_rowcount:
                self.assertEqual(cur.rowcount,0,
                    'cursor.rowcount not being reset to 0 after executing '
                    'no-result statements. It is %s' % cur.rowcount
                    )
        finally:
            con.close()

    def test_rowcount_basic(self):
        "Rowcount should be 1 after singleton insert"
        con, cur = connect_plus_cursor()
        cur.execute("insert into %s values ('Victoria Bitter')" % (
            Booze.name
            ))
        self.failUnless(cur.rowcount in (-1,1))

    def test_fetchall_insert(self):
        "Fetchall returns accurate data"
        con, cur = Booze.create()

        self._insert(con, cur, data=dict(name="Cooper's"))
        self._insert(con, cur, data=dict(name="Victoria Bitter"))
        cur.execute('select name from %s' % Booze.name)
        res = cur.fetchall()
        ls = len(res)
        self.assertEqual(ls, 2,'fetchall wrong number of rows: %s' % ls)
        beers = [res[0][0],res[1][0]]
        beers.sort()
        self.assertEqual(beers[0],"Cooper's",
            'cursor.fetchall retrieved incorrect data')
        self.assertEqual(beers[1],"Victoria Bitter",
            'cursor.fetchall retrieved incorrect data')

    @requires('scrollable_cursors', 'amiracle')
    def test_scrollable_basic(self):
        "Scrollable cursors are set with cursor.set_scrollable"
        #TODO: Is this how we want scrollable cursors to behave?
        con, cur = connect_plus_cursor()
        cur.set_scrollable(True)
        cur.set_scrollable(False)
    
    @requires('scrollable_cursors', 'amiracle')
    def test_scrollable(self):
        "Scrollable cursors stay open after commits (test is broken)"
        #TODO: Is this how we want scrollable cursors to behave?  Fix test.
        con, cur = Booze.create()
        
        data = [ (1, 'a'), (2, 'bb'), (3, 'ccc') ]
        self.cs.executemany("INSERT INTO %s VALUES (?, ?)" % 
            Booze.name, data)
        cur.set_scrollable(1)
        self.cs.execute("SELECT * FROM %s" % Booze.name)
        rows = self.cs.fetchmany( len(data) )
        for i in range( len(data) ):
            self.assertEqual(tuple(rows[i]),data[i])

    beer_samples = [
        'Carlton Cold',
        'Carlton Draft',
        'Mountain Goat',
        'Redback',
        'Victoria Bitter',
        'XXXX'
        ]

    def _populate(self, cur):
        """ Insert rows to setup the DB for the fetch tests. """
        for s in self.beer_samples:
            cur.execute("insert into %s values ('%s')" % 
                (Booze.name, s))
        #TODO: commit?

    def test_executemany(self):
        '''Insert multiple rows using executemany'''
        con, cur = Booze.create()
        try:
            largs = [ ("Cooper's",) , ("Boag's",) ]
            margs = [ {'beer': "Cooper's"}, {'beer': "Boag's"} ]
            if self.driver.paramstyle == 'qmark':
                cur.executemany(
                    'insert into %s values (?)' % Booze.name, largs)
            elif self.driver.paramstyle == 'numeric':
                cur.executemany(
                    'insert into %s values (:1)' % Booze.nmae, largs)
            elif self.driver.paramstyle == 'named':
                cur.executemany(
                    'insert into %s values (:beer)' % Booze.name, margs)
            elif self.driver.paramstyle == 'format':
                cur.executemany(
                    'insert into %s values (%%s)' % Booze.name, largs)
            elif self.driver.paramstyle == 'pyformat':
                cur.executemany(
                    'insert into %s values (%%(beer)s)' % (Booze.name), margs)
            else:
                self.fail('Unknown paramstyle')
            #TODO: Move this to it's own test.  psycopg2 doesn't support
            #self.failUnless(cur.rowcount in (-1,2),
            #    'cursor.rowcount has incorrect value %r' % cur.rowcount
            #    )
            cur.execute('select name from %s' % Booze.name)
            res = cur.fetchall()
            self.assertEqual(len(res),2,
                  'cursor.fetchall retrieved incorrect number of rows'
                  )  
            beers = [res[0][0],res[1][0]]
            beers.sort()
            self.assertEqual(beers[0],"Boag's",'incorrect data retrieved')            
            self.assertEqual(beers[1],"Cooper's",'incorrect data retrieved')
        finally:
            con.close()

    def test_fetchone(self):
        '''Fetchone retrieves row & sets rowcount'''
        con, cur = Booze.create()

        try:
            cur.execute('select name from %s' % Booze.name)
            self.assertEqual(cur.fetchone(),None,
                'cursor.fetchone should return None if a query retrieves '
                'no rows'
                )
            self.failUnless(cur.rowcount in (-1,0))

            cur.execute("insert into %s values ('Victoria Bitter')" 
                        % Booze.name)
            cur.execute('select name from %s' % Booze.name)
            r = cur.fetchone()
            self.assertEqual(len(r),1,
                'cursor.fetchone should have retrieved a single row'
                )
            self.assertEqual(r[0],'Victoria Bitter',
                'cursor.fetchone retrieved incorrect data'
                )
            self.assertEqual(cur.fetchone(),None,
                'cursor.fetchone should return None if no more rows available'
                )
            #TODO: Move this into own test
            if driver_meta.rowcount_reset_empty_fetch:
                self.failUnless(cur.rowcount in (-1,0),
                                "rowcount should be reset after failed fetch")
        finally:
            con.close()

    def test_fetchmany(self):
        '''Fetchmany retrieves rows & sets rowcount'''
        con, cur = Booze.create()

        try:
            self._populate(cur)
            cur.execute('select name from %s' % Booze.name)
            r = cur.fetchmany()
            self.assertEqual(len(r),1,
                'cursor.fetchmany retrieved incorrect number of rows, '
                'default of arraysize is one.'
                )
            cur.arraysize=10
            r = cur.fetchmany(3) # Should get 3 rows
            self.assertEqual(len(r),3,
                'cursor.fetchmany retrieved incorrect number of rows'
                )
            r = cur.fetchmany(4) # Should get 2 more
            self.assertEqual(len(r),2,
                'cursor.fetchmany retrieved incorrect number of rows'
                )
            r = cur.fetchmany(4) # Should be an empty sequence
            self.assertEqual(len(r),0,
                'cursor.fetchmany should return an empty sequence after '
                'results are exhausted'
            )
            #TODO: Move this into it's own test
            if driver_meta.rowcount_reset_empty_fetch:
                self.failUnless(cur.rowcount in (-1,0),
                    "rowcount should be reset after empty fetch")

            # Same as above, using cursor.arraysize
            cur.arraysize=4
            cur.execute('select name from %s' % Booze.name)
            r = cur.fetchmany() # Should get 4 rows
            self.assertEqual(len(r),4,
                'cursor.arraysize not being honoured by fetchmany')
            r = cur.fetchmany() # Should get 2 more
            self.assertEqual(len(r),2)
            r = cur.fetchmany() # Should be an empty sequence
            self.assertEqual(len(r),0)
            if driver_meta.rowcount_reset_empty_fetch:
                self.failUnless(cur.rowcount in (-1,0),
                    "rowcount should be reset after empty fetch")

            cur.arraysize=6
            cur.execute('select name from %s' % Booze.name)
            rows = cur.fetchmany() # Should get all rows
            if driver_meta.sane_rowcount:
              #TODO: Move this to own test.
              self.failUnless(cur.rowcount in (-1,6))
            self.assertEqual(len(rows),6)
            self.assertEqual(len(rows),6)
            rows = [r[0] for r in rows]
            rows.sort()

            # Make sure we get the right data back out
            for i in range(0,6):
                self.assertEqual(rows[i],self.beer_samples[i],
                    'incorrect data retrieved by cursor.fetchmany'
                    )

            rows = cur.fetchmany() # Should return an empty list
            self.assertEqual(len(rows),0,
                'cursor.fetchmany should return an empty sequence if '
                'called after the whole result set has been fetched'
                )
            if driver_meta.rowcount_reset_empty_fetch:
                self.failUnless(cur.rowcount in (-1,0),
                    "rowcount should be reset after empty fetch")

            Barflys.create(con = con, cur = cur)
            cur.execute('select name from %s' % Barflys.name)
            r = cur.fetchmany() # Should get empty sequence
            self.assertEqual(len(r),0,
                'cursor.fetchmany should return an empty sequence if '
                'query retrieved no rows'
                )
            self.failUnless(cur.rowcount in (-1,0),
                "rowcount should be reset after empty fetch")

        finally:
            con.close()

    def test_fetchall(self):
        '''Fetchall retrieves rows & sets rowcount'''
        con, cur = Booze.create()

        try:
            self._populate(cur)
            cur.execute('select name from %s' % Booze.name)
            rows = cur.fetchall()
            self.assertEqual(len(rows),len(self.beer_samples),
                'cursor.fetchall did not retrieve all rows'
                )
            if driver_meta.sane_rowcount:
              #TODO: Move to own test.  BTW, is sane_rowcount really sane_fetchall_rowcount?
              self.failUnless(cur.rowcount in (-1,len(self.beer_samples)))
            rows = [r[0] for r in rows]
            rows.sort()
            for i in range(0,len(self.beer_samples)):
                self.assertEqual(rows[i],self.beer_samples[i],
                'cursor.fetchall retrieved incorrect rows'
                )
            rows = cur.fetchall()
            self.assertEqual(
                len(rows),0,
                'cursor.fetchall should return an empty list if called '
                'after the whole result set has been fetched'
                )
            if driver_meta.sane_rowcount:
              self.failUnless(cur.rowcount in (-1,len(self.beer_samples)))

            #self.executeDDL2(cur)
            cur.execute('select name from %s' % Barflys.name)
            rows = cur.fetchall()
            self.failUnless(cur.rowcount in (-1,0))
            self.assertEqual(len(rows),0,
                'cursor.fetchall should return an empty list if '
                'a select query returns no rows'
                )
        finally:
            con.close()

    @requires('sane_empty_fetch')
    def test_emptyfetch(self):
        """Fetch methods should raise Error if no query issued"""
        con, cur = connect_plus_cursor()
        self.assertRaises(self.driver.Error,cur.fetchone)
        self.assertRaises(self.driver.Error,cur.fetchmany,4)
        self.assertRaises(self.driver.Error, cur.fetchall)

        """ Fetch should still fail after executing queries that can't
        return rows.
        """
        # Create table
        Booze.create(con = con, cur = cur)
        self.assertRaises(self.driver.Error,cur.fetchone)
        self.assertRaises(self.driver.Error,cur.fetchmany,4)
        self.assertRaises(self.driver.Error,cur.fetchall)
  
        # Insert
        cur.execute("insert into %s values ('Victoria Bitter')" % (
            Booze.name))
        self.assertRaises(self.driver.Error,cur.fetchone)

    def test_mixedfetch(self):
        '''Can mix fetchone, fetchmany, and fetchall'''
        con, cur = Booze.create()

        try:
            self._populate(cur)
            cur.execute('select name from %s' % Booze.name)
            rows1  = cur.fetchone()
            rows23 = cur.fetchmany(2)
            rows4  = cur.fetchone()
            rows56 = cur.fetchall()
            if driver_meta.sane_rowcount:
              self.failUnless(cur.rowcount in (-1,6))
            self.assertEqual(len(rows23),2,
                'fetchmany returned incorrect number of rows'
                )
            self.assertEqual(len(rows56),2,
                'fetchall returned incorrect number of rows'
                )

            rows = [rows1[0]]
            rows.extend([rows23[0][0],rows23[1][0]])
            rows.append(rows4[0])
            rows.extend([rows56[0][0],rows56[1][0]])
            rows.sort()
            for i in range(0,len(self.beer_samples)):
                self.assertEqual(rows[i],self.beer_samples[i],
                    'incorrect data retrieved or inserted'
                    )
        finally:
            con.close()

    #TODO: Put this in alien_tech
    #@requires('drop_schema')
    #def test_drop_schema(self):
        #cs = db.cursor()
        #cs.dropschema(object_type="all")
        #db.commit()
        
    #TODO: Put this in alien_tech
    #@requires('blobs', 'lob_file_handler')
    #def test_lob_open(self):
        #from psycopg2 import *
        #dsn = 'host=%s dbname=%s user=%s password=%s' % (
        #       'localhost', 'kskuhlman', 'kskuhlman', 'itsasecret')
        #
        ##blob_type = 'blob'
        #blob_type = 'text'
        #
        ##con = connect('blob_test')
        #con = connect(dsn=dsn)
        #cur = con.cursor()
        #try:
        #    #cur.execute('drop table text_table')
        #    pass
        #except: 
        #    try: 
        #        cur.rollback()
        #    except: 
        #        pass
        #
        #print "Paramstyle", paramstyle
        #cur.execute('create table text_table (mylob %s)' % blob_type)
        #
        #src = open('test_dbapi.py')
        #
        #cur.execute('insert into text_table values(?)', [src.read(),])
        ##SQLite
        ##cur.execute('insert into text_table values(?)', [Binary(src.read()),])
        ##cur.execute('insert into text_table values(?)', [Binary(src),])
        #
        ##Postgres
        #cur.execute('insert into text_table values(%(val)s)', dict(val=Binary(src.read())))
        #print "read() insert successful"
        #cur.execute('insert into text_table values(%(val)s)', dict(val=Binary(src)))
        #print "no read() insert successful"
        #cur.execute('insert into text_table values(mylob = ?)', src)
        #print "no Binary insert successful"

    tableName = "%sblobtst" % table_prefix
    
    def _createBLOBTable(self, con, cs):
        try:
          cs.execute("drop table %s" % self.tableName)
        except:
          con.rollback()
        bt = dbms_meta.typemap.blob
        cs.execute("CREATE TABLE %s ( P1 %s, P2 %s )" % 
            (self.tableName, bt, bt))

    @requires('smart_lob_open')
    def test_blob_smart_open(self):
        """BLOB (file)"""
        con, cs = connect_plus_cursor()
        import os
        self._createBLOBTable(con, cs)
        f = os.tmpfile()
        data = '\xae' * 1024
        f.write(data)
        f.seek(0, 0)
        #print "Paramstyle is: %s" % self.driver.paramstyle
        cs.execute("INSERT INTO %s (P1) VALUES (?)" % self.tableName, f)
        cs.execute("SELECT * FROM %s" % self.tableName)
        rows = cs.fetchone()
        self.assertEqual(str(rows[0]), data)

    #TODO: Fix test to work with more than just pyformat.
    @requires('blob_binary')
    def test_BLOB_fetchmany(self):
        '''Fetchmany works with BLOBs.'''
        con, cs = connect_plus_cursor()
        SIZE = 10
        self._createBLOBTable(con, cs)
        for i in range(SIZE):
            data = OrderedDict()
            data['P1'] = self.driver.Binary(chr(i) * i)
            data['P2'] = self.driver.Binary(chr(i) * (1024-i))

            ps = self.driver.paramstyle
            if ps == 'qmark':
                cs.execute("INSERT INTO %s VALUES (?, ?)" % self.tableName,
                    data.values())
            elif ps == 'numeric':
                cs.execute("INSERT INTO %s VALUES (:1, :2)" % self.tableName, 
                    data.values())
            elif self.driver.paramstyle == 'named':
                cs.execute("INSERT INTO %s VALUES (:%s, :%s)" % self.tableName,
                    data)
            elif ps == 'format':
                cs.execute("INSERT INTO %s VALUES (%%s, %%s)" %  
                    self.tableName, data.values())
            elif ps == 'pyformat':
                cs.execute("INSERT INTO %s VALUES ((%%(P1)s), (%%(P2)s))" %
                    self.tableName, data)
        cs.execute("SELECT * FROM %s" % self.tableName)
        rows = cs.fetchmany(SIZE)


class TestTypesEmbedded(AcuteBase):
    def setUp(self):
        self.con, self.cs = connect_plus_cursor()
        TestTypes.create(con = self.con, cur = self.cs)

    def tearDown(self):
        self.con.rollback()
        TestTypes.drop(con = self.con, cur = self.cs, ignore_errors=True)
        self.con.commit()
        self.con.close()

    def _get_lastrow(self):
        """Return the last row inserted by this process"""
        id_value = self.cs.lastrowid
        self._insert(self.con, self.cs, table=TestTypes,
            data=dict(int1=id_value), stmt_type='select')
        #TODO: Was the ugly hack to insert worth it?  Or should I just not use parammarker here?
        #self.cs.execute('select * from %s where int1 = ?' % self.table, id_value)
        row = self.cs.fetchone()
        return row

    def _get_row(self, table):
        """Return a row from a table.  
        If there's more than one row, it's an error.
        """
        self.cs.execute("select * from %s" % table.name)
        row = self.cs.fetchall()
        cnt = len(row)
        self.assertEqual(cnt, 1, "Invalid row count %s from fetchall" % cnt)
        return row[0]

    def test_date_insert_string(self):
        '''Insert dates using strings'''
        data = dict(date1 = '2007-05-01')
        self._insert(self.con, self.cs, table=TestTypes, data=data)
        #TODO: Weakened this test to str() for psycopg2
        self.assertEqual(str(self._get_row(TestTypes)[2]), data['date1'])

    def test_date_insert(self):
        '''Insert dates using datetime dates'''
        date1_string = '2007-05-01'
        date1 = datetime.date(2007, 05, 01)
        data = dict(date1 = date1)
        self._insert(self.con, self.cs, table=TestTypes, data=data)
        self.assertEqual(str(self._get_row(TestTypes)[2]), date1_string)

    @requires('timestamp_datatype_subsecond')
    def test_timestamp_insert_string(self):
        '''Insert timestamp with subsecond precision using strings'''
        timestamp1 = '2007-05-01 16:00:57.180210'
        timestamp1_datetime = datetime.datetime(
            2007, 05, 01, 16, 00, 57, 180210)
        self._insert(self.con, self.cs, table=TestTypes, 
            data=dict(timestamp1=timestamp1))
        #print "RowID is ", self.cs.lastrowid, "."
        self.assertEqual(str(self._get_row(TestTypes)[3]),timestamp1)
        #self.assertEqual(self._get_lastrow()[3],timestamp1_datetime)

    def test_timestamp_insert(self):
        '''Insert timestamp using datetime's datetime'''
        timestamp1 = datetime.datetime(2007, 05, 01, 11, 03, 13)
        timestamp1_string = '2007-05-01 11:03:13'
        self._insert(self.con, self.cs, table=TestTypes, 
            data=dict(timestamp1=timestamp1))
        if dbms_meta.__class__.__name__ != 'informix':
            self.assertEqual(str(self._get_row(TestTypes)[3]),
                timestamp1_string)
        else:
            self.assertEqual(self._get_row(self.table)[3].isoformat(' '),
                timestamp1_string)
        #self.assertEqual(self._get_lastrow()[3],timestamp1)

    @requires('time_datatype')
    def test_time_insert_string(self):
        '''Insert time using string'''
        time1 = '11:03:13'
        time1_time = datetime.time(11, 03, 13)
        self._insert(self.con, self.cs, table=TestTypes, 
            data=dict(time1=time1))
        #self.assertEqual(self._get_lastrow()[4],time1_time)
        self.assertEqual(str(self._get_row(TestTypes)[4]),time1)

    @requires('time_datatype_time', 'sane_time')
    def test_time_insert(self):
        '''Insert time using datetime's time'''
        data = dict(time1 = datetime.time(11, 3, 13))
        self._insert(self.con, self.cs, table=TestTypes, data=data)
        self.assertEqual(self._get_row(TestTypes)[4],data['time1'])

    @requires('time_datatype_subsecond')
    def test_time_insert_subsecond_string(self):
        'Insert time with subsecond precision using string'
        time1 = '11:03:13.9999'
        data = dict(time1 = time1)
        self._insert(self.con, self.cs, table=TestTypes, data=data)

    @requires('time_datatype_subsecond', 'time_datatype_time')
    def test_time_insert_subsecond(self):
        "Insert time with subsecond precision using datetime's time"
        data = dict(time1 = datetime.time(11, 3, 13, 9999))
        self._insert(self.con, self.cs, table=TestTypes, data=data)

    @requires('time_datatype_time')
    def test_datatypes_multi(self):
        """Insert a multitude of date/time datatypes in one statement
        Uses datetime module.
        """
        data = dict(date1=datetime.date(1970, 4, 1),
           timestamp1=datetime.datetime(2005, 11, 10, 11, 52, 35, 54839),
           time1=datetime.time(23, 59, 59))
        self._insert(self.con, self.cs, table=TestTypes, data=data)
        
    @requires('time_datatype')
    def test_datatypes_multi_string(self):
        """Insert a multitude of date/time datatypes in one statement
        Uses strings.
        """
        data = dict(date1='1970-04-01',
                    timestamp1='2007-05-01 11:03:13',
                    time1='11:03:13')
        self._insert(self.con, self.cs, table=TestTypes, data=data)
        
    def test_None(self):
        '''Handle Python's None as a database null'''
        con, cur = Booze.create()
        try:
            cur.execute('insert into %s values (NULL)' % Booze.name)
            cur.execute('select name from %s' % Booze.name)
            r = cur.fetchall()
            self.assertEqual(len(r),1)
            self.assertEqual(len(r[0]),1)
            self.assertEqual(r[0][0],None,'NULL value not returned as None')
        finally:
            con.close()

class TestSQLProcs(AcuteBase):

    @requires('callproc', 'lower_func')
    def test_callproc(self):
        '''Call a stored procedure (experimental)'''
        con = self._connect()
        try:
            cur = con.cursor()
            r = cur.callproc(driver_meta.lower_func,('FOO',))
            #r = cur.callproc('lower', 'FOO')
            #self.assertNotEqual(r, None)
            #self.assertEqual(len(r),1)
            #self.assertEqual(r[0],'FOO')
            r = cur.fetchall()
            self.assertNotEqual(r, None, 'callproc produced no result set')
            self.assertEqual(len(r),1,'callproc produced no result set')
            self.assertEqual(len(r[0]),1,
                'callproc produced invalid result set'
                )
            self.assertEqual(r[0][0],'foo',
                'callproc produced invalid results'
                )
        finally:
            con.close()

    @requires('callproc', 'procedures', 'procedures.return_values')
    #TODO: IMMED: Add predicate handling to requires decorator
    #@requires('sql_procedure_language==SQL2003')
    def test_callproc_xxx(self):
        """cs.callproc() - IN, OUT, INOUT parameters"""
        con, cs = connect_plus_cursor()
        assert hasattr(cs, 'callproc')
        try:
            cs.execute("drop function cp_test_1")
        except (driver_module.InterfaceError,
               driver_module.OperationalError):
            pass
        if dbms_meta.__class__.__name__ == 'mysql':
            cs.execute("""DROP PROCEDURE IF EXISTS CP_TEST_1""")
            cs.execute("""
                CREATE procedure CP_TEST_1
                (IN P1 text, OUT P2 text, INOUT P3 INTEGER)
                BEGIN
                    set P2 = 'YYY';
                    set P3 = 3;
                END
            """)
        else:
            cs.execute(
                """CREATE PROCEDURE CP_TEST_1
                (IN P1 CHAR(5), OUT P2 VARCHAR(5), INOUT P3 INTEGER)
                LANGUAGE SQL
                BEGIN
                  SET P2 = 'YYY';
                  SET P3 = 3;
                END
            """)
        p2 = None
        p3 = 1
        params = ( 'XXXXX', p2, p3 )
        r = cs.callproc('CP_TEST_1', params)
        #self.assertNotEqual( params, r )
        self.assertEqual('YYY', p2)
        self.assertEqual(3, p3)
        self.assertEqual( ('XXXXX', 'YYY', 3), r )

    #@requires('amiracle')
    #def test_callproc_xxx_resultsets(self):
    #    """cs.callproc() - w/ Result set"""
    #    con, cs = connect_plus_cursor()
    #    cs.execute("CREATE TABLE CP_TEST_TB ( P1 INTEGER )")
    #    SIZE = 100;
    #    for i in range(SIZE):
    #        cs.execute("INSERT INTO CP_TEST_TB VALUES (%s)" % i)
    #
    #    if driver_meta.stored_procedure_language in ['SQL:2003', 'SQL/PL']:
    #        stmt = """CREATE FUNCTION CP_TEST_1
    #           (IN P1 INTEGER)
    #           LANGUAGE SQL
    #           BEGIN
    #              DECLARE CS1 CURSOR WITH RETURN FOR
    #                   SELECT * FROM CP_TEST_TB;
    #              OPEN CS1;
    #           END
    #           """
    #    elif driver_meta.stored_procedure_language in ['PL/pgSQL']:
    #        stmt = """CREATE FUNCTION populate() RETURNS integer AS $$
    #                DECLARE
    #                -- declarations
    #                BEGIN
    #                PERFORM my_function();
    #                END;
    #                $$ LANGUAGE plpgsql;
    #            """
    #    else:
    #        raise Unsupported
    #    cs.execute(stmt)
    #
    #    r = callproc("CP_TEST_1", 1)
    #    self.assertEqual(r, (1, ))
    #    rows = cs.fetchall()
    #    self.assertEqual(len(rows), SIZE)


    def help_nextset_setUp(self,cur):
        ''' Create a procedure called deleteme that returns two result sets,
        first the number of rows in booze then "name from booze"
        '''
        raise NotImplementedError,'Helper not implemented'
        #TODO: Implement this.
        #sql="""
        #    create procedure deleteme as
        #    begin
        #        select count(*) from booze
        #        select name from booze
        #    end
        #"""
        #cur.execute(sql)

    def help_nextset_tearDown(self,cur):
        'If cleaning up is needed after nextSetTest'
        raise NotImplementedError,'Helper not implemented'
        #TODO: Implement this.
        #cur.execute("drop procedure deleteme")

    @requires('amiracle')
    @requires('callproc', 'nextset')
    def test_nextset(self):
        '''Stored procedure calls return result sets'''
        con, cur = Booze.create()
        self._populate(cur)

        try:
            self.help_nextset_setUp(cur)
            cur.callproc('deleteme')
            numberofrows=cur.fetchone()
            assert numberofrows[0]== len(self.beer_samples)
            assert cur.nextset()
            names=cur.fetchall()
            assert len(names) == len(self.beer_samples)
            s=cur.nextset()
            assert s == None,'No more return sets, should return None'
        finally:
            self.help_nextset_tearDown(cur)
            con.close()

if __name__ == '__main__':
    setup_module()
    suite = unittest.TestSuite()

    for test in [
        TestModule,
        TestModuleDatatypes,
        TestConnection, 
        TestCursor,
        TestTypesEmbedded,
        TestSQLProcs,
        ]:
        suite.addTest(unittest.makeSuite(test))

    unittest.TextTestRunner(verbosity=2).run(suite)

