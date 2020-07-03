import os
import sys
from argparse import ArgumentParser, Namespace

from playhouse.sqlite_ext import (
    FTS5Model, FTSModel, RowIDField, SearchField, SqliteExtDatabase,
)

db = SqliteExtDatabase(None)


class PeeweeIndex4(FTSModel):
    rowid = RowIDField()
    text = SearchField()
    source = SearchField(unindexed=True)

    class Meta:
        database = db
        options = {
            'tokenize': 'unicode61 "remove_diacritics=2"',
        }


class PeeweeIndex5(FTS5Model):
    text = SearchField()
    source = SearchField(unindexed=True)

    class Meta:
        database = db
        options = {
            'tokenize': 'unicode61 remove_diacritics 2',
        }


FTS4_SQL = 'create virtual table document_index_4 using fts4(text, source unindexed, tokenize=unicode61 "remove_diacritics=2")'  # noqa: E501

FTS5_SQL = 'create virtual table document_index_5 using fts5(text, source unindexed, tokenize = "unicode61 remove_diacritics 2")'  # noqa: E501


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
    db.create_tables([PeeweeIndex4, PeeweeIndex5])
    for statement in [FTS4_SQL, FTS5_SQL]:
        db.execute_sql(statement)
    for fn in os.listdir(opts.corpus_dir):
        path = os.path.join(opts.corpus_dir, fn)
        with open(path) as fp:
            text = fp.read()
        PeeweeIndex4.insert({'text': text, 'source': fn}).execute()
        PeeweeIndex5.insert({'text': text, 'source': fn}).execute()
        db.execute_sql(
            'insert into document_index_4 (text, source) values (?, ?)', (text, fn)
        )
        db.execute_sql(
            'insert into document_index_5 (text, source) values (?, ?)', (text, fn)
        )


if __name__ == '__main__':
    main()
