import json

import flask
import weber_utils

from weber_utils._compat import string_types

from . import TestCase


class GetRequestInputTest(TestCase):

    def setUp(self):
        super(GetRequestInputTest, self).setUp()
        self.app = flask.Flask(__name__)

    def test_request_input_json(self):
        data = {"a": 2, "b": "c"}
        with self.app.test_request_context(method="POST", data=json.dumps(data), content_type="application/json"):
            self.assertEquals(weber_utils.get_request_input({"a": int, "b": string_types}), data)

    def test_request_input_form(self):
        data = {"a": "2", "b": "c"}
        with self.app.test_request_context(method="POST", data=data):
            self.assertEquals(weber_utils.get_request_input({"a": int, "b": string_types}), {"a": 2, "b": "c"})
