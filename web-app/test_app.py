
import pytest
from app import app  
from unittest.mock import patch, MagicMock

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@patch('pymongo.collection.Collection.insert_one')
def test_index_post(mock_insert, client):
    """Test the index route with POST method."""
    mock_insert.return_value = None  # Mock the insert_one method
    test_data = {"imageData": "data:image/png;base64,TESTDATA"}
    response = client.post("/", json=test_data)
    assert response.status_code == 200
    assert response.json == {"status": "success", "message": "Image uploaded"}

@patch('requests.get')
def test_trigger_processing(mock_get, client):
    """Test the trigger processing route."""
    mock_response = MagicMock()
    mock_response.json.return_value = {"status": "processed"}
    mock_get.return_value = mock_response

    response = client.post("/trigger-processing")
    assert response.status_code == 200
    assert response.json == {"status": "processed"}


@patch('pymongo.collection.Collection.find')
def test_show_processed_image(mock_find, client):
    """Test the show processed image route."""
    # Create a mock for the find().sort().limit().next() chain
    mock_cursor = MagicMock()
    mock_cursor.sort.return_value = mock_cursor
    mock_cursor.limit.return_value = mock_cursor
    mock_cursor.next.return_value = {
        '_id': 1,
        'processed_image': b'fake_image_data'
    }
    
    mock_find.return_value = mock_cursor
    
    response = client.get("/show-processed-image")
    assert response.status_code == 200
    assert 'text/html' in response.content_type

