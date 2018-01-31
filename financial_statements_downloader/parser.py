import re
from configparser import RawConfigParser

from tika import parser

from financial_statements_downloader.data import Data


def parse(data: Data, config: RawConfigParser):
    while True:
        subject = data.get_not_parsed()
        if subject is None:
            break

        for document in subject['documents']:
            path = document['path']

            pdf = parser.from_file(path)
            pdf_content = pdf['content']

            pdf_content = re.sub(r'(,\d\d)', r'\1|', pdf_content)
            pdf_content = re.sub(r'(\d)\s+(\d)', r'\1\2', pdf_content)

            values = {}

            for items in config.items('parser'):
                print(items)
                values[items[0]] = _extract(pdf_content, items[1])

            data.update_parsed(subject['ico'], path, values)


def _extract(content: str, name: str):
    return 1