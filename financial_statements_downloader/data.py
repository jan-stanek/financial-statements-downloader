from tinydb import TinyDB, Query

class Data:
    db: TinyDB

    def __init__(self, file: str):
        self.db = TinyDB(file)

    def import_icos(self, file):
        self.db.purge()

        with open(file) as f:
            self.db.insert_multiple({'ico': ico.strip(), 'invalid': False, 'downloaded': False, 'parsed': False}
                                    for ico in f)

    def get_not_downloaded(self):
        Subject = Query()
        return self.db.get((Subject.downloaded == False) & (Subject.invalid == False))

    def get_not_parsed(self):
        Subject = Query()
        return self.db.get((Subject.parsed == False) & (Subject.invalid == False))

    def update_downloaded(self, ico: str, capital_base: int, insolvency: bool, documents: dict):
        Subject = Query()
        self.db.update({'capital_base': capital_base, 'insolvency': insolvency, documents: documents},
                       Subject.ico == ico) #todo dict

    def update_failed(self, ico):
        Subject = Query()
        self.db.update({'invalid': True},
                       Subject.ico == ico)

    def update_parsed(self, values):
        pass
