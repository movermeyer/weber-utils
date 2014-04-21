import requests

import pytest


@pytest.mark.parametrize("ascending", [True, False])
def test_sort_ascending(webapp, ascending):
    sort_param = "field1" if ascending else "-field1"
    objs = requests.get(webapp.url.add_path("objects").set_query_param("sort", sort_param)).json()["result"]
    expected = sorted(range(webapp.num_objects), reverse=not ascending)
    assert [obj["field1"] for obj in objs] == expected

@pytest.mark.parametrize("forbidden_field", ["field2", "unknown"])
def test_sort_by_forbidden_field(webapp, forbidden_field):
    resp = requests.get(webapp.url.add_path("objects").set_query_param("sort", "field2")).status_code
    assert resp == requests.codes.bad_request
