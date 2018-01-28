from configparser import RawConfigParser
from urllib.request import urlopen
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import re
from financial_statements_downloader.data import Data


PARSER = "html5lib"


def download_data(data: Data, config: RawConfigParser):
    base_url = config.get('downloader', 'base_url')
    search_url = config.get('downloader', 'search_url')

    limit = config.getint('downloader', 'limit_day')

    for i in range(0, limit):
        subject = data.get_not_downloaded()
        ico = subject['ico']

        url = urljoin(base_url, search_url + ico)
        result = urlopen(url)
        bs = BeautifulSoup(result, PARSER)

        extract_link = bs.find('a', text='Úplný výpis')
        if extract_link is None:
            data.update_failed(ico)
            continue

        extract_url = urljoin(base_url, extract_link.get('href'))
        documents_url = urljoin(base_url, bs.find('a', text='Sbírka listin').get('href'))

        capital_base, insolvency = _parse_extract(extract_url)
        documents = _download_documents(base_url, documents_url, config.get('downloader', 'documents_type'))

        data.update_downloaded(ico, capital_base, insolvency, documents)


def _parse_extract(extract_url):
    result = urlopen(extract_url)
    bs = BeautifulSoup(result, "html5lib")
    capital_base = int(bs.find('span', text=re.compile('Základní kapitál'))
                       .parent.parent.parent
                       .contents[3].contents[1].contents[1].contents[2]
                       .text.replace(' ', ''))

    insolvency = bs.find('span', text=re.compile('Údaje o insolvencích')) is not None

    return capital_base, insolvency


def _download_documents(base_url, documents_url, type):
    result = urlopen(documents_url)
    bs = BeautifulSoup(result, PARSER)

    statements = bs.find_all('span', class_='symbol', text=re.compile(type))

    documents = {}

    for statement in statements:
        row = statement.parent.parent.parent

        document_url = urljoin(base_url, row.contents[1].contents[0].get('href'))
        date_created = row.contents[5].text #todo parse

        document_result = urlopen(documents_url)
        document_bs = BeautifulSoup(document_result, PARSER)

        file_url = urljoin(base_url, document_bs.find('th', text=re.compile('PDF podoba')).parent.contents[3].contents[0].get('href'))

        documents[file_url] = date_created

    return documents


