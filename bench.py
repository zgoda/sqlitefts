import sqlite3
import datetime
from argparse import ArgumentParser, Namespace


def get_options() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument('name', metavar='DBNAME', help='Database file name')
    return parser.parse_args()


def run_raw_sql(db_file: str):
    print('Raw SQL benchmark')
    print('=================')
    tables = {
        'di_4_s': 'FTS4, simple',
        'di_4_u': 'FTS4, unicode61',
        'di_5_s': 'FTS5, simple',
        'di_5_u': 'FTS5, unicode61',
    }
    sql = 'select * from {table} where text match ?'
    terms = [
        'github', 'github*',
        'javascript', 'javascript*',
        'framework', 'framework*',
        'toaleta', 'toalet*',
        'piwo', 'piw*',
        'wariat', 'wariat*',
    ]
    for table, description in tables.items():
        with sqlite3.connect(db_file) as cn:
            cr = cn.cursor()
            for term in terms:
                t0 = datetime.datetime.utcnow()
                cr.execute(sql.format(table=table), (term, ))
                delta = (datetime.datetime.utcnow() - t0).total_seconds() * 1000.0
                print(f'{description}: {term}; rows {len(cr.fetchall())}; {delta:.4f}')


def main():
    opts = get_options()
    run_raw_sql(opts.name)


if __name__ == '__main__':
    main()
