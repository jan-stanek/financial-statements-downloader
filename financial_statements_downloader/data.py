from tinydb import TinyDB, Query


class Data:
    db: TinyDB
    query: Query

    def __init__(self, file: str):
        self.db = TinyDB(file)
        self.query = Query()

    def import_icos(self, file: str):
        self.db.purge()

        with open(file) as f:
            self.db.insert_multiple(
                {'ico': ico.strip(), 'invalid': False, 'downloaded': False, 'parsed': False} for ico in f
            )

    def get_not_downloaded(self):
        return self.db.get((self.query.downloaded == False) & (self.query.invalid == False))

    def get_not_parsed(self):
        return self.db.get((self.query.parsed == False) & (self.query.invalid == False))

    def update_downloaded(self, ico: str, capital_base: int, insolvency: bool, documents: list):
        self.db.update(
            {'downloaded': True, 'capital_base': capital_base, 'insolvency': insolvency, 'documents': documents},
            self.query.ico == ico
        )

    def update_failed(self, ico: str):
        self.db.update(
            {'invalid': True},
            self.query.ico == ico
        )

    def update_parsed(self, ico: str, path: str, values: dict):
        self.db.update(
            {'values': values},
            (self.query.ico == ico) & (self.query.documents.file == path)
        )
