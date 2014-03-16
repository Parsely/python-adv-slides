def url_parse(url):
    """Takes a string URL and returns a dictionary of its various parts."""
    
    print "URL IN: " + url

    scheme = url.split("://")[0] + "://"
    remains = url.split("://")[1]
    
    if ":" in remains:
        host = remains.split(":")[0]
        remains = remains.split(":")[1]
        port = remains.split("/", 1)[0]
    else:
        host = remains.split("/", 1)[0]
        if scheme == "http://":
          port = 80
        elif scheme == "https://":
          port = 443
        else: port = None
    
    remains = remains.split("/", 1)[1]
    
    fragment = None
    if "#" in remains:
        fragment = "#" + remains.split("#")[1]
        remains = remains.split("#")[0]
    
    query = None
    if "?" in remains:
        query = "?" + remains.split("?")[1]
        remains = remains.split("?")[0]
    
    path = "/" + remains
    url_dict = {'scheme': scheme, 'host': host, 'port': port, 'path': path, 'query': query, 'fragment': fragment}
    return url_dict
 
 
def url_join(parts):
    """Takes a dictionary of URL parts and returns a valid URL."""
    if parts['port'] == 80 or parts['port'] == 443:
        combined_url = "{scheme}{host}{path}".format(**parts)
    else:
        combined_url = "{scheme}{host}:{port}{path}".format(**parts)

    if parts['query']: combined_url += parts['query']
    if parts['fragment']: combined_url += parts['fragment']
    #would be this clean if I could figure out how to return an empty string when value is None
    #combined_url = "{scheme}{host}{path}{query}{fragment}".format(**parts)

    print "URLOUT: " + combined_url
    return combined_url

# test lines
import fixture
fixture.url_parse = url_parse
fixture.url_join = url_join
from tests import *
