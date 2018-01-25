from urllib.request import urlopen
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import re


ico = ['64573311', '63981432', '28312562']
base_url = 'https://or.justice.cz/ias/ui/'
search_url = 'https://or.justice.cz/ias/ui/rejstrik-$firma?ico='

page = urlopen(search_url + ico[2])
soup = BeautifulSoup(page, "html5lib")

vypis_url = urljoin(base_url, soup.find('a', text='Výpis platných').get('href'))
listiny_url = urljoin(base_url, soup.find('a', text='Sbírka listin').get('href'))

page = urlopen(vypis_url)
soup = BeautifulSoup(page, "html5lib")

zakladni_kapital = int(soup.find('span', text=re.compile('Základní kapitál')).parent.parent.parent.contents[3].contents[1].contents[1].contents[2].text.replace(' ', ''))

insolvence = soup.find('span', text=re.compile('Údaje o insolvencích')) is not None




page = urlopen(listiny_url)
soup = BeautifulSoup(page, "html5lib")

zaverky = soup.find_all('span', class_='symbol', text=re.compile('závěrka'))

for zaverka in zaverky:
    row = zaverka.parent.parent.parent
    link = urljoin(base_url, row.contents[1].contents[0].get('href'))
    vznik = row.contents[5].text
    print(link)
    print(vznik)

    page_file = urlopen(link)
    soup_2 = BeautifulSoup(page_file, "html5lib")

    file_link = urljoin(base_url, soup_2.find('th', text=re.compile('PDF podoba')).parent.contents[3].contents[0].get('href'))
    print(file_link)

print(soup.title.string)
