"""
This package manages the collection of data on the web
and the export of this same data in a certain format.
"""
from typing import Union

from bs4 import BeautifulSoup

from data import web_crawler as crawler


def find_sitemaps_url(url: str) -> Union[list, None]:
    # Try usual case like url/sitemap.xml
    # search in the robots.txt file

    urls = []

    sitemapContent = crawler.retrieveWebContent(crawler.retrieveUrlBase(url), crawler.URL_EXTENSIONS.get('sitemap'))

    # The sitemap file was found
    if sitemapContent is None:
        soup = BeautifulSoup(sitemapContent, 'xml')
        urls = soup.find_all('loc')
    # The robots file was found.
    else:
        # Search into the sitemap if present. if the content of the sitemap does not refer to other sitemaps, return
        # the first sitemap.
        robotContent = crawler.retrieveWebContent(crawler.retrieveUrlBase(url), crawler.URL_EXTENSIONS.get('robots'))
        lines = robotContent.split('\n')
        if len(lines) == 0:
            return None

        for i in range(len(lines) - 1):
            if lines[i].startswith('Sitemap'):
                urls.append(lines[i].split(':')[1].replace(' ', ''))

        # No sitemap has been found for this website.
        if len(urls) == 0:
            print(f'[WARN] No sitemap has been found for the following website: {url}')
            return None

        return robotContent

    return urls if len(urls) > 0 else None


if __name__ == '__main__':
    print(repr(crawler.retrieveWebContent('https://www.chess.com/sitemapindex.xml')))
    # print(repr(find_sitemaps_url('https://developer.mozilla.org/sitemap.xml')))
