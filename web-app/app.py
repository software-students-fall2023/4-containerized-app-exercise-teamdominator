from flask import Flask, render_template
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB
# this need to be changed when using docker for mongodb
client = MongoClient("mongodb://localhost:27017/")
db = client.test


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/visualize_data")
def visualize_data():
    data = db.test.find_one()
    return render_template("visualize_data.html", data=data)


if __name__ == "__main__":
    app.run(debug=True)
