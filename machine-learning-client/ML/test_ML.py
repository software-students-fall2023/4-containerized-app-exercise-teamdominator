import pytest
from unittest.mock import patch, MagicMock
from main import app  # Import your Flask app
import numpy as np
import io

# Configure app for testing
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@patch('main.cv2.dnn.readNet')
@patch('main.open', new_callable=MagicMock)
def test_load_yolo_model(mock_open, mock_read_net):
    # Mock 'open' to return a list of labels
    mock_open.return_value.__enter__.return_value = io.StringIO('label1\nlabel2\nlabel3')

    from main import load_yolo_model

    # Mock behavior
    mock_read_net.return_value = MagicMock()

    # Execute
    net, classes = load_yolo_model('fake_weights', 'fake_config', 'fake_labels')

    # Assertions
    mock_read_net.assert_called_once()
    mock_open.assert_called_once_with('fake_labels', 'r')
    assert len(classes) > 0
    assert net is not None

# Test for process_image function
@patch('main.cv2.dnn.blobFromImage')
def test_process_image(mock_blob_from_image):
    from main import process_image

    # Setup the mock
    mock_net = MagicMock()
    mock_blob = np.zeros((320, 320, 3), dtype=np.uint8)
    mock_blob_from_image.return_value = mock_blob

    # Execute
    outputs, width, height = process_image(mock_net, np.zeros((320, 320, 3), dtype=np.uint8))

    # Assertions
    mock_blob_from_image.assert_called_once()
    assert outputs is not None
    assert width == 320
    assert height == 320

@patch('main.yolo_object_detection')
@patch('main.db')
def test_process_latest_image(mock_db, mock_yolo, client):
    mock_db["image_collection"].find.return_value.sort.return_value.limit.return_value.next.return_value = {
        '_id': '123',
        'image': b'test image data'
    }
    mock_yolo.return_value = b'some processed image data'

    response = client.get('/process-latest-image')
    assert response.status_code == 200
    assert response.json['status'] == 'processed'
