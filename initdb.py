import os
import sys
from argparse import ArgumentParser, Namespace

from models import PeeweeIndex4S, PeeweeIndex4U, PeeweeIndex5S, PeeweeIndex5U, db

SQL_TABLE_STATEMENTS = {
    'fts4_u': 'create virtual table di_4_u using fts4(text, source unindexed, tokenize=unicode61 "remove_diacritics=2")',  # noqa: E501
    'fts4_s': 'create virtual table di_4_s using fts4(text, source unindexed)',
    'fts5_u': 'create virtual table di_5_u using fts5(text, source unindexed, tokenize = "unicode61 remove_diacritics 2")',  # noqa: E501
    'fts5_s': 'create virtual table di_5_s using fts5(text, source unindexed)',
}


def initialize_database(database, name):
    database.init(name, pragmas={'journal_mode': 'wal'})


def get_options() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument('name', metavar='DBNAME', help='Database file name')
    parser.add_argument(
        '-f', '--force', action='store_true', dest='force_overwrite',
        help='Overwrite database if exists',
    )
    parser.add_argument(
        '-c', '--corpus-dir', default='corpus',
        help='Filesystem location of corpus directory [default: %default]',
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
    for statement in SQL_TABLE_STATEMENTS.values():
        db.execute_sql(statement)
    for fn in os.listdir(opts.corpus_dir):
        path = os.path.join(opts.corpus_dir, fn)
        with open(path) as fp:
            text = fp.read()
        for cls in [PeeweeIndex4S, PeeweeIndex4U, PeeweeIndex5S, PeeweeIndex5U]:
            cls.insert({'text': text, 'source': fn}).execute()
        for tbl_name in ['di_4_s', 'di_4_u', 'di_5_s', 'di_5_u']:
            sql = f'insert into {tbl_name} (text, source) values (?, ?)'
            db.execute_sql(sql, (text, fn))


if __name__ == '__main__':
    main()
