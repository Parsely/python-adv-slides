from fixture import url_parse, url_join

def test_basic_url():
    url = "http://www.linkedin.com/in/andrewmontalenti"
    parsed_url = url_parse(url)
    assert parsed_url["scheme"] == "http://"
    assert parsed_url["host"] == "www.linkedin.com"
    assert parsed_url["path"] == "/in/andrewmontalenti"
    assert parsed_url["port"] == 80
    assert parsed_url["fragment"] is None
    assert parsed_url["query"] is None

    
def test_advanced_url():
    url = "http://www.linkedin.com/profile/view?id=13836198&trk=ppro_viewmore#more-123"
    parsed_url = url_parse(url)
    assert parsed_url["fragment"] == "#more-123"
    assert parsed_url["query"] == "?id=13836198&trk=ppro_viewmore"


def test_joining_url():
    url_parts = {
        "scheme": "http://",
        "host": "www.linkedin.com",
        "path": "/profile/view",
        "fragment": "#more-123",
        "query": "?id=13836198&trk=ppro_viewmore",
        "port": 80
    }
    url = "http://www.linkedin.com/profile/view?id=13836198&trk=ppro_viewmore#more-123"
    assert url_join(url_parts) == url, url_join(url_parts)
    url_parts["port"] = 8080
    url = "http://www.linkedin.com:8080/profile/view?id=13836198&trk=ppro_viewmore#more-123"
    assert url_join(url_parts) == url, url_join(url_parts)
    url_parts["scheme"] = "https://"
    url_parts["port"] = 443
    url = "https://www.linkedin.com/profile/view?id=13836198&trk=ppro_viewmore#more-123"
    assert url_join(url_parts) == url
