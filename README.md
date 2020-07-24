# SQLite FTS comparison

[SQLite](https://sqlite.org) provides full text search extensions in 3 forms, the most mature fts3/fts4 and newest fts5. This repository provides insight on usability of these extensions in context of Polish language texts.

Various aspects of FTS extensions can be changed at compile time, but we will use only system provided binaries that are available in Ubuntu 20.04 and Debian 10 because this is what's system provided Python 3 standard library uses, and we will be using only system-provided Python 3.

## Platforms and software versions

The same set of tests will be performed on both platforms using default Python 3 versions.

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

From that it looks SQLite was compiled using the same flags so I will expect the same results. Out of curiosity, I checked how this looks for latest Fedora 32 Server.

### Fedora 32

```shell
python3 -VV
Python 3.8.3 (default, May 29 2020, 00:00:00)
[GCC 10.1.1 20200507 (Red Hat 10.1.1-1)]
```

```shell
sqlite3
SQLite version 3.32.3 2020-06-18 14:00:33
Enter ".help" for usage hints.
Connected to a transient in-memory database.
Use ".open FILENAME" to reopen on a persistent database.
sqlite> PRAGMA compile_options;
COMPILER=gcc-10.1.1 20200507 (Red Hat 10.1.1-1)
DISABLE_DIRSYNC
ENABLE_BYTECODE_VTAB
ENABLE_COLUMN_METADATA
ENABLE_DBSTAT_VTAB
ENABLE_FTS3
ENABLE_FTS3_PARENTHESIS
ENABLE_FTS4
ENABLE_FTS5
ENABLE_JSON1
ENABLE_RTREE
ENABLE_STMTVTAB
ENABLE_UNKNOWN_SQL_FUNCTION
ENABLE_UNLOCK_NOTIFY
HAVE_ISNAN
SECURE_DELETE
THREADSAFE=1
```

## Test scope

The only ORM that explicitly support FTS is [Peewee](http://docs.peewee-orm.com/en/latest/peewee/sqlite_ext.html#sqlite-fts), with others like SQLAlchemy or Pony user has to resort to using *raw* SQL so there is no point in testing them. And since both platforms provide FTS4 there's no way to test FTS3 support using Peewee (and there is no point in testing it with raw access since it's virtually identical wrt search behaviour and the only difference is in performance) so finally scope of tests is as follows:

* FTS4 using tokenizers `simple` and `unicode61` with `remove_diacritics=2`, Python dbapi-2.0 sqlite3 module
* FTS5 using tokenizers `simple` and `unicode61` with `remove_diacritics=2`, Python dbapi-2.0 sqlite3 module
* FTS4 using tokenizers `simple` and `unicode61` with `remove_diacritics=2`, Peewee `FTSModel`
* FTS5 using tokenizers `simple` and `unicode61` with `remove_diacritics=2`, Peewee `FTS5Model`

The meaning of `remove_diacritics=2` is explained in SQLite docs:

> The remove_diacritics option may be set to "0", "1" or "2". The default value is "1". If it is set to "1" or "2", then diacritics are removed from Latin script characters as described above. However, if it is set to "1", then diacritics are not removed in the fairly uncommon case where a single unicode codepoint is used to represent a character with more that one diacritic. For example, diacritics are not removed from codepoint 0x1ED9 ("LATIN SMALL LETTER O WITH CIRCUMFLEX AND DOT BELOW"). This is technically a bug, but cannot be fixed without creating backwards compatibility problems. If this option is set to "2", then diacritics are correctly removed from all Latin characters.

Using `porter` tokenizer does not make much sense for Polish, and `icu` tokenizer is not available on any of test platforms.

## Corpus

The corpus used for testing purpose will be a collection of ~50 blog texts authored by me in years 2013-2020 that can be found on [my blog](https://beergeek.zgodowie.org) pages. This is UTF-8 encoded text rich with IT terms, containing excerpts of computer code and occasional English fragments.

## Test result scoring

The best support for Polish language analysis is provided by Lucene based solutions, like Elasticsearch or Solr. Both of these packages provide Stempel algorythmic analyzer and filter, while Solr also provides dictionary based Morfologik filter and lemmatizer. To score test results we'll be using Elasticsearch 7.8 with Stempel plugin.
