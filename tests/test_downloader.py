from configparser import ConfigParser

import os

from financial_statements_downloader.data import Data
from financial_statements_downloader.downloader import download_data


class FakeData(Data):
    subject = {'ico': '00014028', 'invalid': False, 'downloaded': False, 'parsed': False}

    def __init__(self, file: str):
        pass

    def get_not_downloaded(self):
        subject = self.subject
        self.subject = None
        return subject

    def update_downloaded(self, ico: str, capital_base: int, insolvency: bool, documents: list):
        pass


data = FakeData('')


def test_download_data():
    config = ConfigParser()
    with open('tests/fixtures/configs/config.cfg') as f:
        config.read_file(f)

    download_data(data, config)

    assert os.path.isdir('tests/fixtures/documents/00014028') == True

    files = os.listdir('tests/fixtures/documents/00014028')

    assert len(files) >= 2
    assert 'B 24_SL9_KSCB.pdf' in files
    assert 'B 24_SL57_KSCB.pdf' in files
