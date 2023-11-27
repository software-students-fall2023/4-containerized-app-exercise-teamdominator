import pytest

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index_route(client):
    """Test the index route."""

    # Simulate a GET request to the '/' route
    response = client.get("/")

    # Check if the response is 200 OK
    # We can do more checks here if we want
    assert response.status_code == 200
    assert b"Data from MongoDB" in response.data
