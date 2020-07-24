import os
import sys
from argparse import ArgumentParser, Namespace

from playhouse.sqlite_ext import (
    FTS5Model, FTSModel, RowIDField, SearchField, SqliteExtDatabase,
)

db = SqliteExtDatabase(None)


class PeeweeIndex4U(FTSModel):
    rowid = RowIDField()
    text = SearchField()
    source = SearchField(unindexed=True)

    class Meta:
        database = db
        options = {
            'tokenize': 'unicode61 "remove_diacritics=2"',
        }


class PeeweeIndex4S(FTSModel):
    rowid = RowIDField()
    text = SearchField()
    source = SearchField(unindexed=True)

    class Meta:
        database = db


class PeeweeIndex5U(FTS5Model):
    text = SearchField()
    source = SearchField(unindexed=True)

    class Meta:
        database = db
        options = {
            'tokenize': 'unicode61 remove_diacritics 2',
        }


class PeeweeIndex5S(FTS5Model):
    text = SearchField()
    source = SearchField(unindexed=True)

    class Meta:
        database = db


FTS4_SQL_U = 'create virtual table di_4_u using fts4(text, source unindexed, tokenize=unicode61 "remove_diacritics=2")'  # noqa: E501

FTS4_SQL_S = 'create virtual table di_4_s using fts4(text, source unindexed)'  # noqa: E501

FTS5_SQL_U = 'create virtual table di_5_u using fts5(text, source unindexed, tokenize = "unicode61 remove_diacritics 2")'  # noqa: E501

FTS5_SQL_S = 'create virtual table di_5_s using fts5(text, source unindexed)'  # noqa: E501


def initialize_database(database, name):
    database.init(name, pragmas={'journal_mode': 'wal'})


def get_options() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument('name', metavar='DBNAME', help='Database file name')
    parser.add_argument(
        '-f', '--force', action='store_true', dest='force_overwrite',
        help='Overwrite database if exists'
    )
    parser.add_argument(
        '-c', '--corpus-dir', default='corpus',
        help='Filesystem location of corpus directory [default: corpus]',
    )
    return parser.parse_args()


def main():
    opts = get_options()
    if os.path.exists(opts.name):
        if opts.force_overwrite:
            os.remove(opts.name)
        else:
            sys.exit(f'File {opts.name} exists, use --force to overwrite')
    initialize_database(db, opts.name)
    db.create_tables([PeeweeIndex4S, PeeweeIndex4U, PeeweeIndex5S, PeeweeIndex5U])
    for statement in [FTS4_SQL_S, FTS4_SQL_U, FTS5_SQL_S, FTS5_SQL_U]:
        db.execute_sql(statement)
    for fn in os.listdir(opts.corpus_dir):
        path = os.path.join(opts.corpus_dir, fn)
        with open(path) as fp:
            text = fp.read()
        PeeweeIndex4S.insert({'text': text, 'source': fn}).execute()
        PeeweeIndex4U.insert({'text': text, 'source': fn}).execute()
        PeeweeIndex5S.insert({'text': text, 'source': fn}).execute()
        PeeweeIndex5U.insert({'text': text, 'source': fn}).execute()
        db.execute_sql(
            'insert into di_4_s (text, source) values (?, ?)', (text, fn)
        )
        db.execute_sql(
            'insert into di_4_u (text, source) values (?, ?)', (text, fn)
        )
        db.execute_sql(
            'insert into di_5_s (text, source) values (?, ?)', (text, fn)
        )
        db.execute_sql(
            'insert into di_5_u (text, source) values (?, ?)', (text, fn)
        )


if __name__ == '__main__':
    main()
