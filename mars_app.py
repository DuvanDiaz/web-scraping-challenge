import sys
from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars

sys.setrecursionlimit(2000)
app = Flask(__name__)

mongo = PyMongo(app)


# use pymongo to connect with mongodb server
# client = pymongo.MongoClient('mongodb://localhost:27017')
# db = client.mars_db
# collection = mars_db



# render index.html
# @app.route('/')
# def home():
#     mars = collection.find_one()
#     return render_template("index.html", mars = mars)

# @app.route('/scrape')
# def scrape():
#     scrape_mars.scrape()
#     return redirect('/', code = 302)

@app.route("/")
def index():
    mars = mongo.db.mars_db.find_one()
    return render_template("index.html", mars = mars)

@app.route("/scrape")
def scrape():
    mars = mongo.db.mars_db 
    mars_data = scrape_mars.scrape()
    mars.update({}, mars_data, upsert=True)
    return redirect("http://localhost:27017/", code=302)

if __name__ == "__main__":
    app.run(debug=True)


# if __name__ == "__main__":
#     app.run(debug=True)
