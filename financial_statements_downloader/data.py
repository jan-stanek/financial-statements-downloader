from tinydb import TinyDB, Query


class Data:
    """Object for working with TinyDB.

    It allows create database, import ICOs, return not processed subjects and update information about subject.
    """
    db: TinyDB
    query: Query

    def __init__(self, file: str):
        """Initializes database and query object.

        :param file: path to database file
        :type file: str
        """
        self.db = TinyDB(file)
        self.query = Query()

    def import_icos(self, file: str):
        """Imports ICOs into database.

        :param file: path to ICOs file
        :type file: str
        """
        self.db.purge()

        with open(file) as f:
            self.db.insert_multiple(
                {'ico': ico.strip(), 'invalid': False, 'downloaded': False, 'parsed': False} for ico in f
            )

    def get_not_downloaded(self):
        """Returns one of the subjects which doesn't have invalid ICO and it's documents haven't been downloaded yet.

        :return: subject
        :rtype: dict
        """
        return self.db.get((self.query.downloaded == False) & (self.query.invalid == False))

    def get_not_parsed(self):
        """Returns one of the subjects which doesn't have invalid ICO and it's documents haven't been extracted yet.

        :return: subject
        :rtype: dict
        """
        return self.db.get((self.query.parsed == False) & (self.query.invalid == False))

    def update_downloaded(self, ico: str, capital_base: int, insolvency: bool, documents: list):
        """Updates subject after successful documents download.

        :param ico: updated subjects ICO
        :type ico: str
        :param capital_base: extracted capital base
        :type capital_base: int
        :param insolvency: extracted insolvency status
        :type insolvency: bool
        :param documents: information about downloaded documents
        :type documents: list
        """
        self.db.update(
            {'downloaded': True, 'capital_base': capital_base, 'insolvency': insolvency, 'documents': documents},
            self.query.ico == ico
        )

    def update_failed(self, ico: str):
        """Updates subject if ICO was not found.

        :param ico: updated subjects ICO
        :type ico: str
        """
        self.db.update(
            {'invalid': True},
            self.query.ico == ico
        )

    def update_parsed(self, ico: str, path: str, values: dict):
        """Updates subject after successful parsing document.

        :param ico: updated subjects ICO
        :type ico: str
        :param path: document path
        :type path: str
        :param values: extracted data
        :type values: dict
        """
        self.db.update(
            {'values': values},
            (self.query.ico == ico) & (self.query.documents.file == path)
        )
