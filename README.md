# SQLite FTS comparison

[SQLite](https://sqlite.org) provides full text search extensions in 3 forms, the most mature fts3/fts4 and newest fts5. This repository provides insight on usability of these extensions in context of Polish language texts.

Various aspects of FTS extensions can be changed at compile time, but we will use only system provided binaries that are available in Ubuntu 20.04 and Debian 10 because this is what's system provided Python 3 standard library uses, and we will be using only system-provided Python 3.

## Platform and software versions

### Ubuntu 20.04

```shell
python3 -VV
Python 3.8.2 (default, Apr 27 2020, 15:53:34) 
[GCC 9.3.0]
```

```shell
sqlite3
SQLite version 3.31.1 2020-01-27 19:55:54
Enter ".help" for usage hints.
Connected to a transient in-memory database.
Use ".open FILENAME" to reopen on a persistent database.
sqlite> PRAGMA compile_options;
COMPILER=gcc-9.3.0
ENABLE_COLUMN_METADATA
ENABLE_DBSTAT_VTAB
ENABLE_FTS3
ENABLE_FTS3_PARENTHESIS
ENABLE_FTS3_TOKENIZER
ENABLE_FTS4
ENABLE_FTS5
ENABLE_JSON1
ENABLE_LOAD_EXTENSION
ENABLE_PREUPDATE_HOOK
ENABLE_RTREE
ENABLE_SESSION
ENABLE_STMTVTAB
ENABLE_UNKNOWN_SQL_FUNCTION
ENABLE_UNLOCK_NOTIFY
ENABLE_UPDATE_DELETE_LIMIT
HAVE_ISNAN
LIKE_DOESNT_MATCH_BLOBS
MAX_SCHEMA_RETRY=25
MAX_VARIABLE_NUMBER=250000
OMIT_LOOKASIDE
SECURE_DELETE
SOUNDEX
THREADSAFE=1
USE_URI
```

### Debian 10

```shell
python3 -VV
Python 3.7.3 (default, Dec 20 2019, 18:57:59) 
[GCC 8.3.0]
```

```shell
sqlite3
SQLite version 3.27.2 2019-02-25 16:06:06
Enter ".help" for usage hints.
Connected to a transient in-memory database.
Use ".open FILENAME" to reopen on a persistent database.
sqlite> PRAGMA compile_options;
COMPILER=gcc-8.3.0
ENABLE_COLUMN_METADATA
ENABLE_DBSTAT_VTAB
ENABLE_FTS3
ENABLE_FTS3_PARENTHESIS
ENABLE_FTS3_TOKENIZER
ENABLE_FTS4
ENABLE_FTS5
ENABLE_JSON1
ENABLE_LOAD_EXTENSION
ENABLE_PREUPDATE_HOOK
ENABLE_RTREE
ENABLE_SESSION
ENABLE_STMTVTAB
ENABLE_UNKNOWN_SQL_FUNCTION
ENABLE_UNLOCK_NOTIFY
ENABLE_UPDATE_DELETE_LIMIT
HAVE_ISNAN
LIKE_DOESNT_MATCH_BLOBS
MAX_SCHEMA_RETRY=25
MAX_VARIABLE_NUMBER=250000
OMIT_LOOKASIDE
SECURE_DELETE
SOUNDEX
THREADSAFE=1
USE_URI
```
