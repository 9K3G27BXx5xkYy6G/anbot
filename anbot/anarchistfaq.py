from urllib.request import urlopen
from bs4 import BeautifulSoup

URLS = [
        *[
            f'https://www.anarchistfaq.org/afaq/section{section}.html'
            for section in 'ABCDEFGHIJ'
        ],
        'https://www.anarchistfaq.org/afaq/append2.html'
    ]

def fetch(urls = URLS):
    for url in urls:
        with urlopen(url) as doc:
            soup = BeautifulSoup(doc)
        # sections preceded by <a name=
        paras = []
        for para in soup.find_all('p'):
            strings = []
            for string in para.get_text().split('\n'):
                string = string.strip()
                if string:
                    strings.append(string)
            paras.append(' '.join(strings))
        yield '\n'.join(paras)

if __name__ == '__main__':
    for doc in fetch():
        print(doc)

