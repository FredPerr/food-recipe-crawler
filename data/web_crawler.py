import urllib.request
from urllib.error import HTTPError, URLError
from typing import Union

URL_EXTENSIONS = {"robots": "/robots.txt", "sitemap": "/sitemap.xml"}

def retrieveWebContent(url: str, extension: str = '', encoding: str = 'utf8',
                       useAgent: bool = True) -> Union[None, str]:
    """ Load the html content of a website.

    This function sends a request to a server using the given url with the given extension.
    The distant server can raise an error which will be handled in that function. This will
    cause the return type to be None. Otherwise, the return value will be the content of the
    page.

    :param useAgent:  A boolean value of true to use an agent. This can be helpful in
                      cases were a permission error is raised. The agent used is Mozilla 5.0.
    :param extension: An extension string value appended to the url. This is used
                      to retrieve multiple pages quickly into a website. The default
                      value of the extension is an empty string.
    :param url:       The url of the website's page.
    :param encoding:  The encoding to use for the decoding part. Default is UTF-8.
    :return:          The content of the website as a string.
    """
    try:
        agent_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'} if useAgent else {}
        http_request = urllib.request.Request(url + extension, headers=agent_headers)
        handle = urllib.request.urlopen(http_request)
        content = handle.read()
        handle.close()
        return content.decode(encoding)
    except HTTPError as err:
        print(f'[Error no.{err.code}] Could not read the content of the following url: {url}')
        return None
    except URLError as err:
        print(f'[Error no.{err.errno}] The following URL cannot be found: {url}')
        return None


def retrieveUrlBase(url: str) -> Union[None, str]:
    """ Get the base url of an url which represent the root of the url "path".

    :param url: The url to get the base path from.
    :return: The base of the url or None if the url was not valid.
    """
    urlBaseLastIndex = 0
    slashesCount = 0
    for i in range(len(url) - 1):
        if url[i] == '/':
            slashesCount += 1
            if slashesCount == 3:
                urlBaseLastIndex = i
                break
    if urlBaseLastIndex == 0:
        return None
    return url[:urlBaseLastIndex]
