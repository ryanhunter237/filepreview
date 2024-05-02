from pathlib import PureWindowsPath

import pytest

from filepreview import create_app


@pytest.fixture
def app():
    test_config = {"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"}
    app = create_app(test_config)
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


def test_post_and_get_methods(client):
    # Test POST method
    response = client.post(
        "/api/file",
        json={
            "groupid": "testgroup",
            "filepath": str(PureWindowsPath("C:/Users/User/Documents/test.txt")),
            "md5": "123abc",
        },
    )
    assert response.status_code == 201
    assert response.get_json()["message"] == "File added successfully"

    # # Test GET method
    # response = client.get('/api/files/testgroup')
    # data = response.get_json()
    # assert response.status_code == 200
    # assert len(data) == 1
    # assert data[0]['groupid'] == 'testgroup'
    # assert data[0]['filepath'] == 'path/to/file'
    # assert data[0]['md5'] == '123abc'
