from pathlib import PureWindowsPath
from typing import Iterator

import pytest
from flask import Flask
from flask.testing import FlaskClient, FlaskCliRunner

from filepreview import create_app
from filepreview.models.models import FileData


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


def test_file_api_single_post_and_get(client: FlaskClient):
    # Test POST method
    post_data = {
        "group_id": "testgroup",
        "file_path": str(PureWindowsPath("Documents/test.txt")),
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


def test_file_api_multiple_post_and_get(client: FlaskClient):
    post_data = [
        {"group_id": "gid1", "file_path": "test/path", "md5": "md51"},
        {"group_id": "gid2", "file_path": "test/path/two", "md5": "md52"},
        {"group_id": "gid1", "file_path": "test/path/three", "md5": "md52"},
    ]
    for pd in post_data:
        response = client.post("/api/file", json=pd)
        assert response.status_code == 201
        assert response.get_json()["message"] == "File added successfully"

    response = client.get("/api/files/gid1")
    data = response.get_json()
    assert response.status_code == 200
    assert len(data) == 2
    file_paths = [d["file_path"] for d in data]
    assert sorted(file_paths) == ["test/path", "test/path/three"]
    md5s = [d["md5"] for d in data]
    assert sorted(md5s) == ["md51", "md52"]


def test_file_data_api_single_post(client: FlaskClient, app: Flask):
    # Test POST method
    post_data = {
        "md5": "123abc",
        "num_bytes": 12345,
        "local_path": str(PureWindowsPath("C:/Users/User/Documents/test.txt")),
    }
    response = client.post(
        "/api/file-data",
        json=post_data,
    )
    assert response.status_code == 201
    assert response.get_json()["message"] == "FileData added successfully"
    with app.app_context():
        file_data: FileData = FileData.query.filter_by(md5="123abc").first()
        assert file_data is not None
        assert file_data.num_bytes == post_data["num_bytes"]
        assert file_data.local_path == post_data["local_path"]
