import random
from uuid import uuid1

import requests
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_loopback import FlaskLoopback
from urlobject import URLObject

import pytest
from weber_utils.pagination import paginated_view


class App(object):

    def __init__(self, flask_app):
        super(App, self).__init__()
        self.flask_app = flask_app
        self.loopback = FlaskLoopback(self.flask_app)
        self.hostname = str(uuid1())
        self.url = URLObject("http://{0}".format(self.hostname))

    def activate(self):
        self.loopback.activate_address((self.hostname, 80))

    def deactivate(self):
        self.loopback.deactivate_address((self.hostname, 80))

    def get_page(self, page_size, page):
        response = requests.get(self.url.add_path("objects").set_query_param("page", str(page)).set_query_param("page_size", str(page_size)))
        response.raise_for_status()
        data = response.json()
        assert data["metadata"]["page"] == page
        assert data["metadata"]["page_size"] == page_size
        return data["result"]


@pytest.fixture
def webapp(request):
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
    app.config["PROPAGATE_EXCEPTIONS"] = True

    db = SQLAlchemy(app)

    class Object(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        field1 = db.Column(db.Integer)

    db.create_all()

    @app.route("/objects")
    @paginated_view
    def view_objects():
        return Object.query

    num_objects = 100
    field1_values = list(range(num_objects))
    random.shuffle(field1_values)
    for field1_value in field1_values:
        db.session.add(Object(field1=field1_value))

    db.session.commit()

    returned = App(app)
    returned.num_objects = num_objects
    returned.activate()
    request.addfinalizer(returned.deactivate)

    return returned
