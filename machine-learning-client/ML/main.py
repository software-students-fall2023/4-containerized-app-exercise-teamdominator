import cv2
import numpy as np
import collections



def load_yolo_model(weights, config, labels):
    net = cv2.dnn.readNet(weights, config)
    with open(labels, 'r') as f:
        classes = [line.strip() for line in f.readlines()]
    return net, classes

def process_image(net, image, size=(320, 320), conf_threshold=0.5, nms_threshold=0.4):
    height, width = image.shape[:2]
    blob = cv2.dnn.blobFromImage(image, 1/255.0, size, swapRB=True, crop=False)
    net.setInput(blob)
    layer_names = net.getLayerNames()
    
    out_layers = net.getUnconnectedOutLayers()
    if out_layers.ndim == 1:
        output_layers = [layer_names[i - 1] for i in out_layers]
    else:
        output_layers = [layer_names[i[0] - 1] for i in out_layers]

    outputs = net.forward(output_layers)
    return outputs, width, height


def get_boxes(outputs, width, height, conf_threshold, nms_threshold):
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
    for i in indices:
        if isinstance(i, collections.Iterable):
            i = i[0]
        box = boxes[i]
        x, y, w, h = box
        label = str(classes[class_ids[i]])
        confidence = confidences[i]
        color = [int(c) for c in np.random.uniform(0, 255, 3)]
        cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
        cv2.putText(image, f'{label} {confidence:.2f}', (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)


def yolo_object_detection(image_path, weights, config, labels):
    image = cv2.imread(image_path)
    net, classes = load_yolo_model(weights, config, labels)
    outputs, width, height = process_image(net, image)
    indices, boxes, class_ids, confidences = get_boxes(outputs, width, height, 0.5, 0.4)
    draw_labels(indices, boxes, class_ids, confidences, classes, image)
    cv2.imwrite('detected_objects.jpg', image)

# Replace these paths with the actual paths to your YOLO model files

yolo_weights = 'yolov/yolov3.weights'
yolo_config = 'yolov/yolov3.cfg'
yolo_labels = 'yolov/coco.names'

# Replace with the path to an image you want to process
image_path = 'zidane.jpg'

yolo_object_detection(image_path, yolo_weights, yolo_config, yolo_labels)
