
def _make_dict(scheme, host, port, path, query, fragment):
    """Return a dict like `{"scheme": scheme, "port": port, ...}`."""
    return dict(**vars())


def _default_port_for_scheme(scheme):
    if scheme.startswith("http:"):
        port = 80
    elif scheme.startswith("https:"):
        port = 443
    else:
        port = None
    return port


def url_parse(url):
    """Parses a URL (e.g. "http://lnkd.in/amonta") into parts as dict.

    Example usage:

    >>> parsed = url_parse("http://lnkd.in/amonta")
    >>> parsed["path"]
    '/amonta'
    >>> parsed["port"]
    80

    >>> parsed = url_parse("https://g.co/?a=b#hash")
    >>> parsed["query"]
    '?a=b'
    >>> parsed["fragment"]
    '#hash'
    >>> parsed["scheme"]
    'https://'
    """
    # split off the scheme
    scheme, rest = url.split(":", 1)
    # add back scheme character
    scheme = scheme + "://"
    # skip over "//" characters
    rest = rest[2:]
    # split off the path
    path_char = rest.find("/")
    if path_char == -1:
        # no path found; defaults
        host = rest
        path = None
    else:
        host = rest[0:path_char]
        path = rest[path_char:]
    # set the port, or pick a default
    if ":" in host:
        host, port = host.split(":", 1)
    else:
        port = _default_port_for_scheme(scheme)
    # break query and fragment from path
    query_char = rest.find("?")
    frag_char = rest.find("#")
    if query_char == -1:
        query = None
    else:
        # special cast: query should only be up until
        # fragment if both are included
        if frag_char != -1:
            query = rest[query_char:frag_char]
        else:
            # otherwise, if no fragment found, query is rest
            query = rest[query_char:]
    if frag_char == -1:
        # no fragment found
        fragment = None
    else:
        # fragment always comes last, so it gobbles up rest
        fragment = rest[frag_char:]
    return _make_dict(scheme, host, port, path, query, fragment)


def _set_blank_if_none(d, keys):
    """Sets a given key's value to empty string ('') if its value is `None`."""
    for key in keys:
        if d.get(key, None) is None:
            d[key] = ""


def url_join(parsed_url):
    """Converts dict representing a URL into a string URL.

    Example usage:

    >>> url = dict(
    ... scheme="http://",
    ... host="linkedin.com",
    ... port=80,
    ... path="/amontalenti",
    ... query=None,
    ... fragment=None)
    >>> url_join(url)
    'http://linkedin.com/amontalenti'

    >>> url = dict(
    ... scheme="https://",
    ... host="g.co",
    ... port=443,
    ... path="/",
    ... query="?a=b",
    ... fragment="#hash")
    >>> url_join(url)
    'https://g.co/?a=b#hash'
    """
    # scheme includes "://" already
    base_url = "{scheme}{host}{port}"
    # path leads with "/", query leads with "?", and
    # fragment leads with "#", but they are part of values
    path_part = "{path}{query}{fragment}"
    scheme = parsed_url["scheme"]
    port = parsed_url["port"]
    # handle special default ports (80/443)
    if port == _default_port_for_scheme(scheme):
        # it's the default port, so don't include it
        parsed_url["port"] = ""
    else:
        # it's not the default, so we should include it
        parsed_url["port"] = ":{}".format(port)
    # path, query, and fragment should be blank strings
    # if they are None
    _set_blank_if_none(parsed_url,
                       ["path", "query", "fragment"])
    full_url = base_url + path_part
    url = full_url.format(**parsed_url)
    return url


# test lines
import fixture
fixture.url_parse = url_parse
fixture.url_join = url_join
from tests import *
