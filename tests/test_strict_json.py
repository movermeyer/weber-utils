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

def test_strict_json():
    with pytest.raises(BadRequest):
        strict_json["nonexisting"]
    assert strict_json["string_key"] == "value"

def test_strict_types():
    with pytest.raises(BadRequest):
        strict_json["string_key", int]
    assert strict_json["int_key", int] == 3
    with pytest.raises(BadRequest):
        strict_json["int_key", str]
