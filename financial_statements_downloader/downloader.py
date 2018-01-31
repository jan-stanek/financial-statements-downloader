from configparser import RawConfigParser
from urllib.request import urlopen, urlretrieve, build_opener
from urllib.parse import urljoin, urlparse, parse_qs

import os

import time
from bs4 import BeautifulSoup
import re
from financial_statements_downloader.data import Data

PARSER = "html5lib"
WAIT = 1


def download_data(data: Data, config: RawConfigParser):
    base_url = config.get('downloader', 'base_url')
    search_url = config.get('downloader', 'search_url')

    limit = config.getint('downloader', 'limit_day')

    for i in range(0, limit):
        subject = data.get_not_downloaded()
        ico = subject['ico']

        url = urljoin(base_url, search_url + ico)
        bs = _open_url(url)

        extract_link = bs.find('a', text='Úplný výpis')
        if extract_link is None:
            data.update_failed(ico)
            continue

        extract_url = urljoin(base_url, extract_link.get('href'))
        documents_url = urljoin(base_url, bs.find('a', text='Sbírka listin').get('href'))

        capital_base, insolvency = _parse_extract(extract_url)
        documents = _download_documents(base_url, documents_url, config.get('downloader', 'documents_type'),
                                        config.get('downloader', 'documents_dir'), ico)

        data.update_downloaded(ico, capital_base, insolvency, documents)


def _parse_extract(extract_url):
    bs = _open_url(extract_url)

    capital_base_row = bs.find('span', text=re.compile('Základní kapitál'))
    if capital_base_row is not None:
        capital_base = int(capital_base_row
                           .parent.parent.parent
                           .contents[3].contents[1].contents[1].contents[2]
                           .text.replace(' ', ''))
    else:
        capital_base = None

    insolvency = bs.find('span', text=re.compile('Údaje o insolvencích')) is not None

    return capital_base, insolvency


def _download_documents(base_url, documents_url, type, directory, ico):
    bs = _open_url(documents_url)

    statements = bs.find_all('span', class_='symbol', text=re.compile(type))

    documents = []

    for statement in statements:
        while True:
            row = statement.parent.parent.parent

            document_url = urljoin(base_url, row.contents[1].contents[0].get('href'))
            date_created = row.contents[5].text  # todo parse

            document_bs = _open_url(document_url)

            document_pdf = document_bs.find('th', text=re.compile('PDF podoba'))
            if document_pdf is None:
                break
            file_url = urljoin(base_url, document_pdf.parent.contents[3].contents[0].get('href'))

            document_name = document_bs.find('th', text=re.compile('Značka'))
            name = document_name.parent.contents[3].text
            name = re.sub(r'[\\/*?:"<>|]', "_", name) + ".pdf"

            path = directory + '/' + ico + '/' + name

            if not os.path.exists(os.path.dirname(path)):
                os.makedirs(os.path.dirname(path))

            site = urlopen(file_url)

            if "text/html" in site.getheader('Content-Type'):
                continue

            # urlretrieve(file_url, path)
            f = open(path, "wb")
            content = site.read()
            f.write(content)
            f.close()

            documents.append({
                'file': path,
                'date': date_created
            })

            time.sleep(WAIT)

            break

    return documents


def _open_url(url):
    opener = build_opener()
    opener.addheaders = [
        ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0')]
    response = opener.open(url)
    bs = BeautifulSoup(response, PARSER)
    time.sleep(WAIT)
    return bs
