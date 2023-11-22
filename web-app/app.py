from flask import Flask, render_template
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB
# this need to be changed when using docker for mongodb
client = MongoClient("mongodb://localhost:27017/")
db = client.test  # this is the database name


@app.route('/')
def index():
    # Fetch some data from your MongoDB database
    data = db.test.find_one()  # Replace test

    # Render an HTML template with data
    return render_template('index.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)

