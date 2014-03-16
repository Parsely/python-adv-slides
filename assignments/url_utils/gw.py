 
def url_parse(url):
    """Takes a string URL and returns a dictionary of its various parts."""
    result = {}
    one = url.split("://")
    result["scheme"] = one[0]+"://"
    two = one[1].split("/",1)
    fragment_index = one[1].find("#")
    result["fragment"] = None
    if fragment_index > 0:
        result["fragment"] = one[1][fragment_index:]
    query_index = one[1].find("?")
    result["query"] = None
    if query_index > 0:
        if fragment_index > 0:
            result["query"] = one[1][query_index:fragment_index]
        else:
            result["query"] = one[1][query_index:]
    path_start = one[1].find("/")
    path_end = -1
    if query_index > path_end:
        path_end = query_index
    elif fragment_index > path_end:
        path_end = fragment_index
    else:
        path_end = len(one[1])
    result["port"] = 80
    port_start = one[1].find(":")
    if port_start > -1:
      port_end = one[1].find("/")
      result["port"] = one[1][port_start:port_end]
    result["host"] = two[0]
    result["path"] = one[1][path_start:path_end]
    print result
    return result
 
 
def url_join(parsed_url):
    """Takes a dictionary of URL parts and returns a valid URL."""
    port = ""
    if parsed_url["port"] != 80 and parsed_url["port"] != 443:
        port = ":{}".format(parsed_url["port"])
    result = "{}{}{}{}{}{}".format(parsed_url["scheme"],parsed_url["host"],port,parsed_url["path"],parsed_url["query"],parsed_url["fragment"])
    print result
    return result

# test lines
import fixture
fixture.url_parse = url_parse
fixture.url_join = url_join
from tests import *
