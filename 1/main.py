import re
from typing import Optional, List

import typer

from crawler import parse_pages

HTTP_REGEXP = re.compile("^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$")
REQUIRED_PAGES_PARSED = 100


def main(args: List[str]) -> Optional[str]:
    for url in args:
        m = re.match(HTTP_REGEXP, url)
        if not m:
            print(f"URL {url} does not match http regexp. Try another url")
            return

    j = 0
    for i, url in enumerate(args):
        pages, pages_parsed = parse_pages(url, REQUIRED_PAGES_PARSED)
        curr_page = 0
        while pages_parsed < REQUIRED_PAGES_PARSED:
            new_pages, new_pages_parsed = parse_pages(pages[curr_page][0], REQUIRED_PAGES_PARSED - pages_parsed)
            pages.extend(new_pages)
            pages_parsed += new_pages_parsed
            curr_page += 1

        for page_url, page in pages:
            with open(f"file_{j}", "w", encoding="utf-8") as outfile:
                outfile.write(page)

            with open("index.txt", "a", encoding="utf-8") as indexfile:
                indexfile.write(f"{j} - {page_url}\n")

            j += 1

    return "success"


if __name__ == "__main__":
    typer.run(main)
