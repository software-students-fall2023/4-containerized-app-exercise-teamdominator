from flask import Flask, jsonify, render_template, request
import pymongo
import base64
import requests

app = Flask(__name__)

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://mongodb:27017/")
db = client.test


@app.route("/", methods=["GET", "POST"])
def index():
    """Endpoint to upload and store image data."""
    if request.method == "POST":
        data = request.get_json()
        image_data = data.get('imageData')

        if image_data:
            image_data = image_data.split(',')[1]  # Remove Data URL part
            image_binary = base64.b64decode(image_data)
            try:
                db["image_collection"].insert_one({'image': image_binary})
            except Exception as e:
                print(f"Error inserting into database: {e}")
                return jsonify({"status": "error", "message": "Failed to upload image"})

        return jsonify({"status": "success", "message": "Image uploaded"})

    return render_template("index.html")


@app.route('/trigger-processing', methods=['POST'])
def trigger_processing():
    """Trigger image processing using the machine-learning client."""
    response = requests.get('http://machine-learning-client:5001/process-latest-image')
    return jsonify(response.json())


@app.route('/show-processed-image')
def show_processed_image():
    """Display the most recently processed image."""
    processed_image_doc = db["processedImageCollection"].find().sort('_id', -1).limit(1).next()
    encoded_image = base64.b64encode(processed_image_doc['processed_image']).decode('utf-8')
    image_data_url = f"data:image/png;base64,{encoded_image}" if processed_image_doc else None

    return render_template("display_image.html", image_data_url=image_data_url)


@app.route("/visualize_data")
def visualize_data():
    """Visualize data from the database."""
    data = db.test.find_one()
    return render_template("visualize_data.html", data=data)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
