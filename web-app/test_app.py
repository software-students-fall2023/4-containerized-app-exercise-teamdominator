import base64

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


## new tests but not passed
def test_index_post_route(client):
    """Test POST request to the index route."""
    sample_image_data = 'data:image/png;base64,' + base64.b64encode(b'test image data').decode()
    response = client.post("/", json={'imageData': sample_image_data})
    assert response.status_code == 200
    assert response.json['status'] == 'success'

def test_trigger_processing_route(client, mocker):
    """Test the trigger-processing route."""
    mocker.patch('requests.get', return_value=MockResponse())
    response = client.post('/trigger-processing')
    assert response.status_code == 200
    # Add more assertions based on expected response

def test_show_processed_image_route(client):
    """Test the show-processed-image route."""
    response = client.get('/show-processed-image')
    assert response.status_code == 200
    assert b'<img src=' in response.data

def test_visualize_data_route(client):
    """Test the visualize_data route."""
    response = client.get('/visualize_data')
    assert response.status_code == 200
    # Add more assertions based on expected content

class MockResponse:
    """Mock response for external service calls."""
    def json(self):
        return {'status': 'success', 'message': 'Processed image'}

if __name__ == "__main__":
    pytest.main()