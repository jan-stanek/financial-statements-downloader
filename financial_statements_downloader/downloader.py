import os
import re
import time
from configparser import RawConfigParser
from urllib.parse import urljoin
from urllib.request import urlopen, build_opener

from bs4 import BeautifulSoup

from financial_statements_downloader.data import Data

PARSER = "html5lib"
"""BeautifulSoup parser."""

WAIT = 1
"""Wait seconds after requests."""


def download_data(data: Data, config: RawConfigParser):
    """Downloads information about subject and documents and stores them into database.

    :param data: data object
    :type data: Data
    :param config: config fro
    :param config: RawConfigParser
    :return:
    """
    base_url = config.get('downloader', 'base_url')
    search_url = config.get('downloader', 'search_url')

    download_extract = config.getboolean('downloader', 'download_extract')
    download_documents = config.getboolean('downloader', 'download_documents')

    documents_type = config.get('downloader', 'documents_type')
    documents_dir = config.get('downloader', 'documents_dir')

    limit = config.getint('downloader', 'limit_day')

    for i in range(0, limit):
        subject = data.get_not_downloaded()
        if subject == None:
            break

        ico = subject['ico']

        url = urljoin(base_url, search_url + ico)
        bs = _open_url(url)

        extract_link = bs.find('a', text='Úplný výpis')  # find extract link
        if extract_link is None:
            data.update_failed(ico)
            continue

        extract_url = urljoin(base_url, extract_link.get('href'))
        documents_url = urljoin(base_url, bs.find('a', text='Sbírka listin').get('href'))  # find documents link

        if download_extract:
            capital_base, insolvency = _parse_extract(extract_url)
        else:
            capital_base = None
            insolvency = None

        if download_documents:
            documents = _download_documents(base_url, documents_url, documents_type, documents_dir, ico)
        else:
            documents = None

        data.update_downloaded(ico, capital_base, insolvency, documents)


def _parse_extract(extract_url: str):
    """
    Parses information from extract.

    :param extract_url: extract url
    :type extract_url: str
    :return: capital base and insolvency
    """
    bs = _open_url(extract_url)

    capital_base_row = bs.find('span', text=re.compile('Základní kapitál'))  # find base capital row
    if capital_base_row is not None:
        capital_base = int(capital_base_row
                           .parent.parent.parent
                           .contents[3].contents[1].contents[1].contents[2]
                           .text.replace(' ', ''))
    else:
        capital_base = None

    insolvency = bs.find('span', text=re.compile('Údaje o insolvencích')) is not None  # check if contains insolvency

    return capital_base, insolvency


def _download_documents(base_url: str, documents_url: str, type: str, directory: str, ico: str):
    """Finds and downloads documents.

    :param base_url: base url
    :type base_url: str
    :param documents_url: documents page url
    :type documents_url: str
    :param type: selected documents type
    :type type: str
    :param directory: documents directory
    :type directory: str
    :param ico: ICO
    :type ico: str
    :return: array of documents
    """
    bs = _open_url(documents_url)

    statements = bs.find_all('span', class_='symbol', text=re.compile(type))  # find all documents of type

    documents = []

    for statement in statements:
        while True:
            row = statement.parent.parent.parent

            document_url = urljoin(base_url, row.contents[1].contents[0].get('href'))  # extract url of file page
            date_created = row.contents[5].text  # extracts document creation date

            document_bs = _open_url(document_url)

            document_pdf = document_bs.find('th', text=re.compile('PDF podoba'))  # find download link
            if document_pdf is None:
                break
            file_url = urljoin(base_url, document_pdf.parent.contents[3].contents[0].get('href'))

            document_name = document_bs.find('th', text=re.compile('Značka'))  # extract document name
            name = document_name.parent.contents[3].text
            name = re.sub(r'[\\/*?:"<>|]', "_", name) + ".pdf"

            path = directory + '/' + ico + '/' + name

            if not os.path.exists(os.path.dirname(path)):  # crate folders if not exist
                os.makedirs(os.path.dirname(path))

            site = urlopen(file_url)

            if "text/html" in site.getheader('Content-Type'):  # check if file is returned, if not try get link again
                continue

            f = open(path, "wb")  # download file
            content = site.read()
            f.write(content)
            f.close()

            documents.append({
                'file': path,
                'date': date_created
            })

            time.sleep(WAIT)  # wait

            break

    return documents


def _open_url(url: str):
    """Opens url, creates BeutifulSoup object and waits.

    :param url: url to get
    :type url: str
    :return: BeautifulSoup object
    """
    opener = build_opener()
    opener.addheaders = [
        ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0')
    ]
    response = opener.open(url)
    bs = BeautifulSoup(response, PARSER)
    time.sleep(WAIT)
    return bs
