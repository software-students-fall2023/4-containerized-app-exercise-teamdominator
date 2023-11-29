from flask import Flask, jsonify, request
import pymongo
import cv2
import base64
import numpy as np
import collections

app = Flask(__name__)
client = pymongo.MongoClient("mongodb://mongodb:27017/")  # Docker service name for MongoDB
db = client.test


def load_yolo_model(weights, config, labels):
    """Load YOLO model from given weights, config, and labels files."""
    net = cv2.dnn.readNet(weights, config)
    with open(labels, 'r') as f:
        classes = [line.strip() for line in f.readlines()]
    return net, classes


def process_image(net, image, size=(320, 320), conf_threshold=0.5, nms_threshold=0.4):
    """Process an image using YOLO model."""
    height, width = image.shape[:2]
    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, size, swapRB=True, crop=False)
    net.setInput(blob)
    layer_names = net.getLayerNames()
    out_layers = net.getUnconnectedOutLayers()

    output_layers = [layer_names[i - 1] for i in out_layers.flatten()]
    outputs = net.forward(output_layers)

    return outputs, width, height


def get_boxes(outputs, width, height, conf_threshold, nms_threshold):
    """Get bounding boxes from YOLO model outputs."""
    class_ids, confidences, boxes = [], [], []
    for output in outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > conf_threshold:
                center_x, center_y, w, h = (detection[0:4] * np.array([width, height, width, height])).astype('int')
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)
    return indices, boxes, class_ids, confidences


def draw_labels(indices, boxes, class_ids, confidences, classes, image):
    """Draw labels and bounding boxes on the image."""
    for i in indices:
        i = i[0] if isinstance(i, collections.Iterable) else i
        box = boxes[i]
        x, y, w, h = box
        label = str(classes[class_ids[i]])
        confidence = confidences[i]
        color = [int(c) for c in np.random.uniform(0, 255, 3)]
        cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
        cv2.putText(image, f'{label} {confidence:.2f}', (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)


def yolo_object_detection(image_binary, weights, config, labels):
    """Perform YOLO object detection on the given image."""
    net, classes = load_yolo_model(weights, config, labels)
    image_np = np.frombuffer(image_binary, np.uint8)
    image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
    outputs, width, height = process_image(net, image)
    indices, boxes, class_ids, confidences = get_boxes(outputs, width, height, 0.5, 0.4)
    draw_labels(indices, boxes, class_ids, confidences, classes, image)
    _, buffer = cv2.imencode('.png', image)
    encoded_image = buffer.tobytes()
    return encoded_image


yolo_weights = 'yolov/yolov3.weights'
yolo_config = 'yolov/yolov3.cfg'
yolo_labels = 'yolov/coco.names'


@app.route('/process-latest-image', methods=['GET'])
def process_latest_image():
    """Process the latest image stored in MongoDB."""
    latest_image_doc = db["image_collection"].find().sort('_id', -1).limit(1).next()
    if latest_image_doc and 'image' in latest_image_doc:
        processed_image = yolo_object_detection(latest_image_doc['image'], yolo_weights, yolo_config, yolo_labels)
        db["processedImageCollection"].insert_one({
            'original_image_id': latest_image_doc['_id'],
            'processed_image': processed_image
        })
        return jsonify({"status": "processed"})
    return jsonify({"status": "no image to process"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
