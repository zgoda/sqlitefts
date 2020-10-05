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
