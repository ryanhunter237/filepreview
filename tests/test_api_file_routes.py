from pathlib import PureWindowsPath, PurePath, PurePosixPath
from typing import Iterator

import pytest
from flask import Flask
from flask.testing import FlaskClient, FlaskCliRunner

from filepreview import create_app
from filepreview.main.models import FileData, File


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


@pytest.mark.parametrize(
    "post_data",
    [
        {
            "group_id": "testgroup",
            "directory": str(PureWindowsPath("User/Documents/test.txt").parent),
            "filename": PureWindowsPath("User/Documents/test.txt").name,
            "md5": "123abc",
        },
        {
            "group_id": "AnotherGroup",
            "directory": str(PurePosixPath("Projects/Files/sample.txt").parent),
            "filename": PurePosixPath("Projects/Files/sample.txt").name,
            "md5": "456def",
        },
        {
            "group_id": "thirdGroup",
            "directory": str(PureWindowsPath("picture.jpg").parent),
            "filename": PureWindowsPath("picture.jpg").name,
            "md5": "789ghi",
        },
    ],
)
def test_file_api_single_post(client: FlaskClient, app: Flask, post_data: dict):
    response = client.post(
        "/api/file",
        json=post_data,
    )
    assert response.status_code == 201
    assert response.get_json()["message"] == "File added successfully"

    with app.app_context():
        query_args = {
            "group_id": post_data["group_id"].lower(),
            "directory": PurePath(post_data["directory"]).as_posix(),
            "filename": post_data["filename"],
        }
        file: File = File.query.filter_by(**query_args).first()
        assert file is not None
        assert file.md5 == post_data["md5"].lower()


@pytest.mark.parametrize(
    "post_data",
    [
        {
            "md5": "123abc",
            "num_bytes": 12345,
            "local_path": str(PureWindowsPath("C:/Users/User/Documents/test.txt")),
        },
        {
            "md5": "456DEF",
            "num_bytes": 0,
            "local_path": str(PurePosixPath("/test/home/Desktop/file.png")),
        },
    ],
)
def test_file_data_api_single_post(client: FlaskClient, app: Flask, post_data: dict):
    response = client.post(
        "/api/file-data",
        json=post_data,
    )
    assert response.status_code == 201
    assert response.get_json()["message"] == "FileData added successfully"

    with app.app_context():
        file_data: FileData = FileData.query.filter_by(
            md5=post_data["md5"].lower()
        ).first()
        assert file_data is not None
        assert file_data.num_bytes == post_data["num_bytes"]
        assert file_data.local_path == PurePath(post_data["local_path"]).as_posix()
