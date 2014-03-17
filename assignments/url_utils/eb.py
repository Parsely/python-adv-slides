# eb's impl

class URLParseError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "URL parse error: {}".format(self.message)


def url_parse(*args):
    """Takes a string URL and returns a dictionary of its various parts."""
    ret = {"scheme": None, "host": None, "path": None, "port": None, "fragment": None, "query": None, "userinfo": None}

    if len(args) == 0:
        return ret
    url = args[0]

    if "://" not in url:
        raise URLParseError("Missing scheme")

    scheme_rest = url.split("://")
    # scheme, *rest = url.split("://")  # py3 only
    ret["scheme"], rest = scheme_rest[0].lower(), scheme_rest[1]
    ret["port"] = 80 if ret["scheme"] == "http" else 443 if ret["scheme"] == "https" else None

    if "/" not in rest:
        raise URLParseError("Missing authority")

    authority_rest = rest.split("/", 1)
    authority, path_query_fragment = authority_rest[0], "/" + authority_rest[1]

    userinfo = authority.split("@")[0] if "@" in authority else None

    # avoid "if @ in authority" by using replace
    host_port = authority.replace("{}@".format(userinfo), "")

    port = host_port.split(":")[1] if ":" in host_port else None
    if port is not None:
        if not port.isdigit():
            raise URLParseError("Invalid port: {}".format(port))
        ret["port"] = int(port)

    ret["query"] = path_query_fragment.split("?")[1].split("#")[0] if "?" in path_query_fragment else None
    ret["fragment"] = path_query_fragment.split("#")[1] if "#" in path_query_fragment else None
    ret["host"] = host_port.split(":")[0]
    ret["userinfo"] = userinfo
    ret["path"] = path_query_fragment.split("?")[0].split("#")[0]

    return ret


def url_join(*args):
    """Takes a dictionary of URL parts and returns a valid URL."""
    in_dict = args[0] if len(args) >= 1 else None
    if not in_dict:
        return ""

    scheme = in_dict["scheme"]
    userinfo = port = query = fragment = ""

    _userinfo = in_dict.get("userinfo", None)
    userinfo = "{}@".format(_userinfo) if _userinfo else ""

    _query = in_dict.get("query", None)
    query = "?{}".format(_query) if _query else ""

    _fragment = in_dict.get("fragment", "")
    fragment = "#{}".format(_fragment) if _fragment else ""

    _port = in_dict.get("port", "")
    if _port:
        if (scheme == "https" and _port != 443) or (scheme == "http" and _port != 80):
            port = ":{}".format(_port)

    return "{scheme}://{userinfo}{host}{port}{path}{query}{fragment}".format(
        scheme=scheme, userinfo=userinfo,
        host=in_dict["host"], port=port, path=in_dict["path"],
        query=query, fragment=fragment
    )

# test lines
import fixture
fixture.url_parse = url_parse
fixture.url_join = url_join
from tests import *
