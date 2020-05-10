import urllib.request
from urllib.error import HTTPError, URLError
from typing import Union

from bs4 import BeautifulSoup

from log_system import error, warn, info

URL_EXTENSIONS = {"robots": "/robots.txt", "sitemap": "/sitemap.xml"}


def retrieveWebContent(url: str, extension: str = '', encoding: str = 'utf8',
                       agent_headers: Union[None, dict] = None) -> Union[str, None]:
    """ Load the html content of a website.

    This function sends a request to a server using the given url with the given extension.
    The distant server can raise an error which will be handled in that function. This will
    cause the return type to be None. Otherwise, the return value will be the content of the
    page.

    :param agent_headers: The user agent to use while requesting the content
                          cases were a permission error is raised. The agent used is Mozilla 5.0.
    :param extension:     An extension string value appended to the url. This is used
                          to retrieve multiple pages quickly into a website. The default
                          value of the extension is an empty string.
    :param url:           The url of the website's page.
    :param encoding:      The encoding to use for the decoding part. Default is UTF-8.
    :return:              The content of the website as a string. If the content could not be
                          reached, it returns None.
    """
    combined_url = url + extension
    try:

        if agent_headers is None:
            agent_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}

        http_request = urllib.request.Request(combined_url, headers=agent_headers)
        handle = urllib.request.urlopen(http_request)
        content = handle.read()
        handle.close()
        return content.decode(encoding)
    except HTTPError as err:
        error(f'Could not read the content of the following url: {combined_url}', err.code)
        return None
    except URLError as err:
        error(f'The following URL could not be found: {combined_url}', err.errno)
        return None


def retrieveUrlBase(url: str) -> Union[None, str]:
    """ Get the base url of an url which represent the root of the url "path".

    :param url: The url to get the base path from.
    :return:    The base of the url or None if the url was not valid.
    """

    if not url.endswith('/'):
        url += '/'

    urlBaseLastIndex = 0
    slashesCount = 0
    for i in range(len(url)):
        if url[i] == '/':
            slashesCount += 1
            if slashesCount == 3:
                urlBaseLastIndex = i
                break
    if urlBaseLastIndex == 0:
        warn(f'Could not find the following URL: {url}')
        return None
    return url[:urlBaseLastIndex]


def find_sitemaps_url(url: str) -> Union[list, None]:
    """Search for the url(s) of the sitemap(s) of a website.

    First, this function searches using the a common url used for
    the sitemap which is 'www.website.com/sitemap.xml'. If did not
    work, it tries to search in the robots.txt file of the website.
    The search is done with a depth value of 1. This means that if
    a sitemap was found and that it represents a list of sitemaps,
    only the first sitemap will be listed.

    :param url: The url to search the sitemaps into. It is possible
                to add an url that have been extended.
    :return:    The list of the found sitemaps or None if an error was
                raised or None was found.
    """
    urls = []

    urlBase = retrieveUrlBase(url)

    # The website url base could not be found.
    if urlBase is None:
        return None

    sitemapContent = retrieveWebContent(urlBase, URL_EXTENSIONS.get('sitemap'))

    # The sitemap file was found and will search into it.
    if sitemapContent is not None:
        soup = BeautifulSoup(sitemapContent, 'xml')
        tag = 'loc'
        urls = soup.find_all(tag)
        for i in range(len(urls)):
            urls[i] = str(urls[i])[len(tag) + 2: -len(tag) - 3]
    # The robots file was found.
    else:
        info('Searching into robots.txt file')
        # Search into the sitemap if present. if the content of the sitemap does not refer to other sitemaps, return
        # the first sitemap.
        robotContent = retrieveWebContent(urlBase, URL_EXTENSIONS.get('robots'))

        if robotContent is None:
            warn('robots.txt file could not be retrieved.')
            return None

        lines = robotContent.split('\n')
        if len(lines) == 0:
            return None

        for i in range(len(lines)):
            if lines[i].startswith('Sitemap'):
                urls.append(lines[i].split(':', 1)[1].replace(' ', ''))

        # No sitemap has been found for this website.
        if len(urls) == 0:
            warn(f'No sitemap has been found for the following website: {url}')
            return None

        # Test the sitemap links to see if they are sitemap links themselves.

    return urls if len(urls) > 0 else None
