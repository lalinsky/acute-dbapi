# Introduction #
Comparison of test support by several DB-API implementations.

| Test Name | psycopg2 | pysqlite2 | mysqldb |
|:----------|:---------|:----------|:--------|
| Required exceptions are in the defined heirachy. | Pass     | Pass      | Pass    |
| Driver defines apilevel | Pass     | Pass      | Pass    |
| Can connect to database | Pass     | Pass      | Pass    |
| Driver defines paramstyle | Pass     | Pass      | Pass    |
| Driver defines threadsafety | Pass     | Pass      | Pass    |
| Module defines BINARY | Pass     | Fail      | Pass    |
| Module supports Binary | Pass     | Pass      | Pass    |
| Module defines DATETIME | Pass     | Fail      | Pass    |
| Module supports Date and DateFromTicks | Pass     | Pass      | Pass    |
| Module supports DateFromTicks | Pass     | Pass      | Pass    |
| Module defines NUMBER | Pass     | Fail      | Pass    |
| Module defines ROWID | Pass     | Fail      | Pass    |
| Module defines STRING | Pass     | Fail      | Pass    |
| Module supports Time and TimeFromTicks | Pass     | Pass      | Pass    |
| Module supports TimeFromTicks | Pass     | Pass      | Pass    |
| Module supports Timestamp and TimestampFromTicks | Pass     | Pass      | Pass    |
| Module supports TimestampFromTicks | Pass     | Pass      | Pass    |
| Module's date is equivalent to datetime's date | Pass     | Pass      | Pass    |
| Module's time attribute is equivalent to datetime's time | Pass     | Pass      | Pass    |
| Module's Timestamp attribute is equivalent to datetime's datetime | Pass     | Pass      | Pass    |
| Connection objects should include the exceptions as attributes (optional) | Pass     | Pass      | Pass    |
| Connection should fail using bogus database | Pass     | Fail      | Pass    |
| Connection should fail using bogus password | Pass     | Fail      | Pass    |
| Connection should fail using bogus username | Pass     | Fail      | Pass    |
| Can't commit, execute, or close a closed connection | Pass     | Fail      | Pass    |
| Can't close a closed connection | Pass     | Fail      | Pass    |
| Can't commit a closed connection | Pass     | Pass      | Pass    |
| Commit must be defined, even if it doesn't do anything | Pass     | Pass      | Pass    |
| Consecutive commits should be successfull | Pass     | Pass      | Pass    |
| Connections need to be able to create cursors | Pass     | Pass      | Pass    |
| Connection should fail using blank password | Pass     | Fail      | Pass    |
| Rollback must work or throw NotSupportedError. | Pass     | Pass      | Pass    |
| Consecutive rollbacks should be successfull | Pass     | Pass      | Pass    |
| Successful connect and close | Pass     | Pass      | Pass    |
| Fetchmany works with BLOBs. | Pass     | Pass      | Pass    |
| Cursor must define arraysize | Pass     | Pass      | Pass    |
| BLOB (file) | Fail     | Fail      | Fail    |
| Connections must have cursor method | Pass     | Pass      | Pass    |
| A cursor can read it's own uncommited data | Pass     | Pass      | Pass    |
| Cursor description describes columns correctly | Pass     | Pass      | Pass    |
| Fetch methods should raise Error if no query issued | Pass     | Fail      | Fail    |
| Insert multiple rows using executemany | Pass     | Pass      | Pass    |
| Fetchall retrieves rows & sets rowcount | Pass     | Pass      | Pass    |
| Fetchall returns accurate data | Pass     | Pass      | Pass    |
| Fetchmany retrieves rows & sets rowcount | Pass     | Pass      | Pass    |
| Fetchone retrieves row & sets rowcount | Pass     | Pass      | Pass    |
| Can mix fetchone, fetchmany, and fetchall | Pass     | Pass      | Pass    |
| Rowcount matches the number of rows inserted | Pass     | Pass      | Pass    |
| Rowcount should be 1 after singleton insert | Pass     | Pass      | Pass    |
| Insert works with cursor.setinputsize | Pass     | Pass      | Pass    |
| Insert works with cursor.setoutputsize | Pass     | Pass      | Fail    |
| Handle Python's None as a database null | Pass     | Pass      | Pass    |
| Insert a multitude of date/time datatypes in one statement using datetime | Pass     | Fail      | Pass    |
| Insert a multitude of date/time datatypes in one statement using strings | Pass     | Pass      | Pass    |
| Insert dates using datetime dates | Pass     | Pass      | Pass    |
| Insert dates using strings | Pass     | Pass      | Pass    |
| Insert time using datetime's time | Pass     | Fail      | Fail    |
| Insert time using string | Pass     | Pass      | Pass    |
| Insert time with subsecond precision using datetime's time | Pass     | Fail      | Pass    |
| Insert time with subsecond precision using string | Pass     | Pass      | Pass    |
| Insert timestamp using datetime's datetime | Pass     | Pass      | Pass    |
| Insert timestamp with subsecond precision using strings | Pass     | Pass      | Fail    |
| Stored procedure calls return result sets | Fail     | Fail      | Fail    |


