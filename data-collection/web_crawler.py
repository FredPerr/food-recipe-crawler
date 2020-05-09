import urllib.request
from urllib.error import HTTPError
from typing import Union

URL_EXTENSIONS = {"robots.txt": "/robots.txt"}


def retrieveWebContent(url: str, encoding: str = 'utf8', extension: str = '') -> Union[None, str]:
    """ Load the html content of a website.

    This function sends a request to a server using the given url with the given extension.
    The distant server can raise an error which will be handled in that function. This will
    cause the return type to be None. Otherwise, the return value will be the content of the
    page.

    :param extension: An extension string value appended to the url. This is used
                      to retrieve multiple pages quickly into a website. The default
                      value of the extension is an empty string.
    :param url:       The url of the website's page.
    :param encoding:  The encoding to use for the decoding part. Default is UTF-8.
    :return:          The content of the website as a string.
    """
    try:
        handle = urllib.request.urlopen(url + extension)
        content = handle.read()
        handle.close()
    except HTTPError as err:
        print(f'[Error no.{err.code}] Could not read the content of the following url: {url}')
        return None
    return content.decode(encoding)


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
