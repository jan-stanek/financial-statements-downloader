import re
from configparser import RawConfigParser

from tika import parser

from financial_statements_downloader.data import Data


def parse(data: Data, config: RawConfigParser):
    """Parses all subjects documents.

    :param data: data object
    :type data: Data
    :param config: config from config file
    :type config: RawConfigParser
    """
    while True:
        subject = data.get_not_parsed()
        if subject is None:  # break if no not processed subject exists
            break

        for document in subject['documents']:
            path = document['file']

            pdf = parser.from_file(path)

            try:
                pdf_content = pdf['content']
                pdf_content = re.sub(r'(,\d\d)', r'\1|', pdf_content)  # insert separator behind number
                pdf_content = re.sub(r'(\d)\s+(\d)', r'\1\2', pdf_content)  # remove spaces between numbers
            except TypeError:
                pdf_content = ""

            values = {}

            for items in config.items('parser'):
                values[items[0]] = _extract(pdf_content, items[1])

            data.update_parsed(subject['ico'], path, values)


def _extract(content: str, name: str):
    """Extracts information from document content.

    :param content: document text content
    :type content: str
    :param name: item to extract name
    :type name: str
    :return: parsed number
    """
    try:
        splitted_content = content.split(name)
        content_behind = splitted_content[1]
        trimmed_number = content_behind.split('|')[1]
        parsed = float(trimmed_number.replace(',', '.'))
    except IndexError:
        parsed = None
    return parsed
