import json

from flask import Flask
from werkzeug.exceptions import BadRequest

import pytest
from weber_utils import strict_json


@pytest.fixture(autouse=True, scope="module")
def json_post(request):
    returned = Flask(__name__).test_request_context("/path", headers={"Content-type": "application/json"}, data=json.dumps({"string_key": "value", "int_key": 3}))
    returned.__enter__()
    request.addfinalizer(lambda: returned.__exit__(None, None, None))
    return returned

def test_nonexisting_key():
    with pytest.raises(BadRequest):
        strict_json["nonexisting"]

def test_string_key_no_explicit_type():
    assert strict_json["string_key"] == "value"

def test_invalid_type():
    with pytest.raises(BadRequest):
        strict_json["string_key", int]

    with pytest.raises(BadRequest):
        strict_json["int_key", str]

def test_type_checking_int():
    assert strict_json["int_key", int] == 3

def test_get_with_default():
    assert strict_json.get("nonexisting", None) is None
    assert strict_json.get("nonexisting", 3) == 3

def test_get_with_default_no_type_checking():
    assert strict_json.get(("nonexisting", int), "default") == "default"

def test_get_with_default_type_checking():
    assert strict_json.get(("int_key", int), "default") == 3
    assert strict_json.get(("string_key", str), 31337) == "value"

    with pytest.raises(BadRequest):
        strict_json.get(("int_key", str), "default")
