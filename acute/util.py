""" Utility functions for the acute DBAPI testsuite """
import config

def import_module(driver_name):
    """ Import a database module by name.  SQLite requires special handling.
    There may be others.. if so, please add them here!
    """
    if driver_name not in ['sqlite3', 'pysqlite2']:
        driver_module = __import__(driver_name)
    else:
        try:
            # SQLite is only included in python 2.5 & above. Previously
            # it was external & named "pysqlite2"
            from sqlite3 import dbapi2 as driver_module
        except ImportError:
            from pysqlite2 import dbapi2 as driver_module
    return driver_module

class OrderedDict(dict): 
    'A simplistic OrderedDict implementation.'
    def __init__(self):
        # No reason to accept kw parms, because they'd be a regular dict & their
        #  order wouldn't be maintained.

        # Save keys to a list so we can preserve order
        self._keylist = []
    
    def __setitem__(self, key, value):
        if not self.has_key(key):
            self._keylist.append(key)
        dict.__setitem__(self, key, value)

    def keys(self):
        return self._keylist

    def values(self):
        return [self.get(key) for key in self._keylist]

    def items(self):
        return [(key, self.get(key)) for key in self._keylist]

    def __str__(self):
        xx = ["%s: %s" % (repr(key), repr(value)) for (key, value) 
                  in self.items()]
        rr = '{'+ ', '.join(xx) +'}'
        return rr

def attr(value, doc = None, conformance_level = 0):
    """Factory function to generate fancy attributes that can be annotated"""
    base = type(value)
    if base == bool:
        # bool class can't be used as a base, so we make one that can.
        class MyBool(int):
            def __str__(self):
                return str(bool(self))
            __repr__ = __str__ 
        base = MyBool

    class FancyAttr(base): 
        pass 

    fa = FancyAttr(value)
    fa.__doc__ = doc
    fa.conformance_level = conformance_level
    return fa

def find_public_atrs(obj):
    """Find the public attributes of an object.
    private attributes have a leading underscore ("_")
    """
    atrs = dir(obj)
    return [atr for atr in atrs if not atr.startswith('_')]


import drivers
driver_meta = getattr(drivers, config.driver_name)()
driver_module = import_module(config.driver_name)

def connect(connection_info=None, connection_method='default'):
    if connection_info == None:
        connection_info = config.ConnectionInfo()

    args, kwargs = driver_meta.convert_connect_args(connection_info)

    try:
        con = driver_module.connect(*args, **kwargs)
    except AttributeError:
        raise("No connect method found in driver module")
    return con

def connect_plus_cursor(connection_info=None, connection_method='default'):
    con = connect(connection_info, connection_method)
    try:
        cs = con.cursor()
    except AttributeError:
        raise("No cursor method found on connection")
    return con, cs

class TableBase(object):
    """A base class for tables.  Defines create & drop methods
    that abstract away concerns about the table already/not
    existing, and whether you need to commit afterwards (some dbs
    have transactional ddl, and other's don't. Default is False.)
    """

    transactional_ddl = True 

    @classmethod
    def create(cls, con=None, cur=None, drop_existing = True):
        """Create a table. 
        Optionally drop any existing one first (default is True)
        Can use an existing connection or cursor if supplied, 
           otherwise it will create new ones.
        """
        if not con:
            con, cur = connect_plus_cursor()
        if drop_existing:
            cls.drop(con, cur, ignore_errors = True)

        cur.execute(cls.ddl)

        if cls.transactional_ddl:
            con.commit()
        return con, cur

    @classmethod
    def drop(cls, con, cur, ignore_errors = True):
        """Given a connection & cursor, drop a table.
        Optionally, ignore errors that occurred in the process.
        Commit changes when done.
        """
        if not con:
            con, cur = connect_plus_cursor()
        try:
            cur.execute('drop table %s' % cls.name)
        except:
            if not ignore_errors:
                raise
        if cls.transactional_ddl or 1==1:
            con.commit()
        return con, cur
 
