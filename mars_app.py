from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

# use pymongo to connect with mongodb server
client = pymongo.MongoClient('mongodb://localhost:27017')
db = client.mars_db
collection = mars_db
# Flask instance
app = Flask(__name__)


# render index.html
@app.route('/')
def home():
    mars = collection.find_one()
    return render_template("index.html", mars = mars)

@app.route('/scrape')
def scrape():
    scrape_mars.scrape()
    return redirect('/', code = 302)


if __name__ == "__main__":
    app.run(debug=True)
    