def url_parse(*args):
    """Takes a string URL and returns a dictionary of its various parts."""
    url = args[0]
    url_parts = {
        "scheme": None,
        "port": None,
        "host": None,
        "path": None,
        "query": None,
        "fragment": None
    }

    scheme, url_sans_scheme = url.split("://")
    url_parts["scheme"] = scheme + "://" # We stripped it off with the split, add it back
    host, request = url_sans_scheme.split("/",1)

    # Find out what host and port is
    if ":" in host:
        # We have a port in the host string
        url_parts["host"],url_parts["port"] = host.split(":")
    else:
        url_parts["host"] = host
        if url_parts["scheme"] == "https://":
            url_parts["port"] = 443
        else:
            url_parts["port"] = 80

    # Determine if query is made
    query_fragment = ''
    if "?" in request:
        path, query_fragment = request.split("?")
        url_parts["path"] = "/" + path # Again, split removed the /
    else:
        url_parts["path"] = "/" + request # Again, split removed the /

    # Determine query fragments
    if "#" in query_fragment:
        query,fragment = query_fragment.split("#")
        url_parts["fragment"] = "#" + fragment
        # Handle case where we have a # but no ?
        if query:
            url_parts["query"] = "?" + query
    else:
        # Ensure not empty string, because we'll return None in that case
        if query_fragment:
            url_parts["query"] = "?" + query_fragment

    return url_parts


def url_join(*args):
    """Takes a dictionary of URL parts and returns a valid URL."""
    url_parts = args[0]
    port = ''
    if not (url_parts["port"] == 80 or url_parts["port"] == 443):
         port = ":%i"  % (url_parts["port"])

    return url_parts["scheme"] + url_parts["host"] + port +  url_parts["path"] + url_parts["query"] + url_parts["fragment"]

# test lines
import fixture
fixture.url_parse = url_parse
fixture.url_join = url_join
from tests import *
