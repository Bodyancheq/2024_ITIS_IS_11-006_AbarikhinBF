from typing import Tuple, List

import requests
import random
from time import sleep
import re
from bs4 import BeautifulSoup
from lxml.html.clean import Cleaner
from urllib.parse import urlparse, urljoin

cleaner = Cleaner(javascript=True, style=True)

CLEANR = re.compile('<(.|\n)*?>')
CLEAN_NEWL = re.compile('\n\t*(\n\t*)+')
REQUIRED_WORDS = 1000

visited_pages = dict()

HEADERS = [{'user-agent': 'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)'},
           {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'},
           {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'},
           {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}]


def parse_page(url: str) -> str:
    print(f"[parsing] {url}")
    response = requests.get(url, headers=HEADERS[random.randint(0, 3)])
    print(f"[status-code] {response.status_code}")
    sleep(random.uniform(0.75, 1.25))
    html_content = response.text

    return html_content


def parse_pages(url: str, pages_left=100) -> Tuple[List[Tuple[str, str]], int]:
    # returns: list of page urls with their contents, number of parsed pages
    pages_parsed = 0
    resulting_pages = list()

    html_content = parse_page(url)
    soup = BeautifulSoup(html_content, 'lxml')
    links = [urlparse(urljoin(url, a.get('href'))) for a in soup.find_all('a', href=True)]
    links = [link.scheme + "://" + link.netloc + link.path for link in links]

    cleaned_text = cleaner.clean_html(html_content)
    cleaned_text = re.sub(CLEANR, '', cleaned_text)
    cleaned_text = re.sub(CLEAN_NEWL, '\n', cleaned_text)
    if len(cleaned_text.split()) >= 1000:
        pages_parsed += 1
        resulting_pages.append((url, cleaned_text))
        print(f"Added page {url} to res pages. Res pages len: {len(resulting_pages)}")

    visited_pages[url] = links

    for link in links:
        if pages_parsed == pages_left:
            return resulting_pages, pages_parsed

        if link not in visited_pages.keys():
            html_content = parse_page(link)
            cleaned_text = cleaner.clean_html(html_content)
            cleaned_text = re.sub(CLEANR, '', cleaned_text)
            cleaned_text = re.sub(CLEAN_NEWL, '\n', cleaned_text)
            if len(cleaned_text.split()) >= REQUIRED_WORDS:
                pages_parsed += 1
                resulting_pages.append((link, cleaned_text))
                print(f"Added page {link} to res pages. Res pages len: {len(resulting_pages)}")

            visited_pages[url] = links

    return resulting_pages, pages_parsed
