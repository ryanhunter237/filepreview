from pathlib import PureWindowsPath
from typing import Iterator

import pytest
from flask import Flask
from flask.testing import FlaskClient, FlaskCliRunner

from filepreview import create_app


@pytest.fixture
def app() -> Iterator[Flask]:
    test_config = {"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"}
    app = create_app(test_config)
    yield app


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()


@pytest.fixture
def runner(app: Flask) -> FlaskCliRunner:
    return app.test_cli_runner()


def test_post_and_get_methods(client: FlaskClient):
    # Test POST method
    post_data = {
        "groupid": "testgroup",
        "filepath": str(PureWindowsPath("C:/Users/User/Documents/test.txt")),
        "md5": "123abc",
    }
    response = client.post(
        "/api/file",
        json=post_data,
    )
    assert response.status_code == 201
    assert response.get_json()["message"] == "File added successfully"

    # Test GET method
    response = client.get("/api/files/testgroup")
    data = response.get_json()
    assert response.status_code == 200
    assert len(data) == 1
    for key in post_data:
        assert data[0][key] == post_data[key]
