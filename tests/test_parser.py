from configparser import ConfigParser

import os

from financial_statements_downloader.data import Data
from financial_statements_downloader.parser import parse


class FakeData(Data):
    subject = {'ico': '00014028',
               'invalid': False,
               'downloaded': True,
               'parsed': False,
               'documents': [{'file': 'tests/fixtures/statements/test.pdf'}]
               }

    def __init__(self, file: str):
        pass

    def get_not_parsed(self):
        subject = self.subject
        self.subject = None
        return subject

    def update_parsed(self, ico: str, path: str, values: dict):
        self.result = values

    def update_failed(self, ico: str):
        pass


data = FakeData('')


def test_download_data():
    config = ConfigParser()
    with open('tests/fixtures/configs/config.cfg') as f:
        config.read_file(f)

    parse(data, config)

    assert data.result['vlastni_kapital'] == 57793320.34
    assert data.result['cizi_zdroje'] == 4545126.47

