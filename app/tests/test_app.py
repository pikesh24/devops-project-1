import pytest
from app import app as flask_app


@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as c:
        yield c


def test_home(client):
    res = client.get("/")
    assert res.status_code == 200
    assert b"running" in res.data


def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert b"healthy" in res.data


def test_data(client):
    res = client.get("/data")
    assert res.status_code == 200
    assert b"items" in res.data


def test_error_endpoint(client):
    res = client.get("/error")
    assert res.status_code == 500


def test_metrics(client):
    res = client.get("/metrics")
    assert res.status_code == 200
    assert b"app_request_count_total" in res.data
